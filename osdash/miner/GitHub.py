#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import datetime
import json
import os
import sys
import urllib.parse
from string import Template

# External imports
import pandas
import requests

#
# Define basic parameters for GitHub API
#

# GitHub API v3 REST endpoint
REST_URL: str = "https://api.github.com/"
# GitHub API v4 GraphQL endpoint
GRAPHQL_URL: str = "https://api.github.com/graphql"
# GitHub API query success response code
SUCCESS_CODE: int = 200
# Requested results per page for each API response
PER_PAGE: int = 100
# Set search depth when getting list of changed files in commits
COMMIT_FILE_DEPTH: int = 3

#
# Define query-making functions
#

# Function to return appropriate query headers given authentication token
def get_headers(api: str, token: str) -> dict: 
    if api == "REST":
        rest_headers: dict = {"Accept": "application/vnd.github.v3+json",
                              "Authorization": f"token {token}"}
        return rest_headers
    elif api == "GraphQL":
        graphql_headers: dict = {"Authorization": f"token {token}"}
        return graphql_headers
    else:
        print(f"ERROR: Please specify API type 'REST' or 'GraphQL'", file=sys.stderr)
        sys.exit(1)

# Function for making queries
def make_query(query: str, token: str): 
    # See if it is a REST query
    if (REST_URL in query) and (not GRAPHQL_URL in query):
        print(f"Looks like a REST query...")
        rest_headers: dict = get_headers(api="REST", token=token)
        query_response: requests.models.Response = requests.get(url=query,
                               headers=rest_headers)
        if query_response.status_code == SUCCESS_CODE:
            return query_response
        else:
            raise Exception(f"Problem with query with return code {query_response.status_code}.")
    # Basic potato check if query looks like GraphQL
    elif ("{" in query) and ("}" in query):
        print(f"Looks like a GraphQL query...")
        graphql_headers: dict = get_headers(api="GraphQL", token=token)
        query_response: requests.models.Response = requests.post(url=GRAPHQL_URL, 
                                                          json={"query": query}, 
                                                          headers=graphql_headers)
        if query_response.status_code == SUCCESS_CODE:
            return query_response
        else:
            raise Exception(f"Problem with query with return code {query_response.status_code}.")
    else:
        print(f"ERROR: Query does not look like REST or GraphQL...", file=sys.stderr)

# Parse GitHub URL to get its "owner" and "name" components
def parse_url(url: str) -> dict:
    """
    For example, given `url="https://github.com/octocat/Hello-World/"`, it 
    would be parsed by `urllib.parse.urlparse()` into components, of which the
    path component can be split into the "owner" and "name", i.e. "octocat" and
    "Hello-World".
    """
    parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    repo: dict = {
        # Get the path component of a `urlparse()`ed URL which looks like
        # "/octocat/Hello-World", then split it by "/" where first part would 
        # be "owner", second part would be "name". 
        # E.g. https://github.com/octocat/Hello-World would have owner 
        # "octocat" and name "Hello-World".
        "owner": getattr(parsed_url, "path").split(sep="/")[1],
        "name": getattr(parsed_url, "path").split(sep="/")[2]
    }
    return repo

# Check rate limits
def check_rate_limit(token):
    query_rate_limit = """
    {
        rateLimit {
            remaining
            resetAt
        }
    }
    """
    results = make_query(query=query_rate_limit, token=token).json()["data"]["rateLimit"]
    remaining = results["remaining"]
    resetAt = results["resetAt"]
    print(f"GitHub API queries remaining: {remaining}", file=sys.stderr)
    print(f"    This quota will reset at: {resetAt}", file=sys.stderr)
    try:
        assert results["remaining"] >= 1000
    except AssertionError:
        print(f"Warning: Only {remaining} queries remaining", file=sys.stderr)

#
# Functions for retrieving different types of metadata
#

# Get branches
def get_branches(repo: dict, token: str):
    """
    Use GraphQL API
    `repo` is a dictionary with two keys "owner" and "name" which are parsed 
    from the repository's full URL with `parse_url()`
    """
    # Fetch data

    # Track if there is a next page of results
    query_has_next_page: bool = True
    # Track results page number
    query_page: int = 1
    # Create a pagination cursor
    end_cursor: str = "null" # "null" because there is no cursor for first query
    # Create empty list of branches to populate from query results
    branches: list = []
    # Create a string template for branches query
    query_branches_template = Template(
    """
    {
    repository(owner: "$owner", name: "$name") {
        refs(first: $per_page, refPrefix: "refs/heads/", after: $after) {
            nodes {
                    name
                }
            pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }
    """
    )

    while query_has_next_page:
        print(f"Getting page {query_page} of branches list", file=sys.stderr)
        # Prepare and execute GraphQL query
        query_branches = query_branches_template.substitute(owner=repo["owner"], 
                                                            name=repo["name"], 
                                                            per_page=PER_PAGE,
                                                            after=end_cursor)
        results = make_query(query=query_branches, token=token).json()["data"]["repository"]["refs"]
        # Get names of branches from query results and append to known branches list
        for node in results["nodes"]:
            branches.append(node["name"])
        # See if there are more pages to retrieve
        query_has_next_page = results["pageInfo"]["hasNextPage"]
        # If so, prepare for next loop iteration
        if query_has_next_page:
            end_cursor = results["pageInfo"]["endCursor"]
            end_cursor = f'"{end_cursor}"' # Add extra quotes to form correct query
            query_page = query_page + 1

    # Print total number of branches
    print(f"Number of branches: {len(branches)}", file=sys.stderr)

    # Format into ForgeFed model

    return branches

# Get commits via REST API
def get_commits_3(repo: dict, since: str, token: str):
    """
    Use GitHub's v3 REST API
    `repo` is a dictionary with two keys "owner" and "name" which are parsed 
    from the repository's full URL with `parse_url()`

    NOTE: THE REST API ONLY RETURNS COMMITS FROM THE DEFAULT BRANCH
    """
    # Fetch data

    # Construct query string
    query_string: str = str(f"{REST_URL}" + "repos/" + f'{repo["owner"]}' + "/" + f'{repo["name"]}' + "/commits")
    # Start with first page
    page: int = 1
    # Append pagination parameters to query
    query_string: str = f"{query_string}?per_page={PER_PAGE}&page={page}"
    # Initialise an empty list to hold query results
    commits: list = list()
    
    # Send queries as long as there are more pages of results
    get_next_page: bool = True
    while get_next_page: 
        response: requests.models.Response = make_query(query=query_string, token=token)
        # See if there is a next page of results
        try:
            'rel="next"' in response.headers["Link"]
        except KeyError:
            # If there's only one page of results, then there is no "Link" item
            # in the response header, so don't go to next page and save results.
            get_next_page = False
            # Add results from this loop iteration to commits list
            commits.extend(response.json())
        else:
            # If there are multiple pages of results, then there will be
            # "rel=next" in the response header "Link". So increment page
            # counter and save current result.
            if 'rel="next"' in response.headers["Link"]:
                page = page + 1
                query_string: str = f"{query_string}?per_page={PER_PAGE}&page={page}"
            else: 
                # Stop if the response header's "Link" section doesn't show a 
                # next page.
                get_next_page = False
            # Add results from this loop iteration to commits list
            commits.extend(response.json())

    # Format into ForgeFed model
    
    return commits

# Get commits from GraphQL API
def get_commits_4(repo: dict, since: str, token: str):
    """
    Use GitHub's v4 GraphQL API
    """
    pass

# Get commit file changes
def get_file_changes():
    """
    Use REST API
    """
    # Fetch data

    # Format into ForgeFed model
    
    pass

# Get issues
def get_issues():
    """
    Use GraphQL API
    """
    # Fetch data

    # Format into ForgeFed model
    
    pass

#
# Main logic for making GitHub queries
#

def GitHub(repo_list: pandas.core.frame.DataFrame, token: str) -> pandas.core.frame.DataFrame:
    """
    docstring
    """
    print(f"Begin GitHub adapter")

    # Create empty DataFrame to hold mined data
    mined_data: pandas.core.frame.DataFrame = repo_list[["repo_url", "last_mined"]]

    # For each repository (row) in `repo_list`, mine data at its URL
    # Use itertuples() because it seems to be much faster than iterrows()
    # Reference: https://stackoverflow.com/a/10739432/186904
    # TODO: Consider using Pandas's apply() instead: https://stackoverflow.com/a/30566899/186904
    for repo in repo_list.itertuples(): 
        # Since itertuples() returns data of namedtuple type, use getattr() to 
        # access items in each row
        # Reference: https://medium.com/@rinu.gour123/python-namedtuple-working-and-benefits-of-namedtuple-in-python-276d679b2e9c
        print(f"Processing: " + getattr(repo, "repo_url"))
        repo_url: str = str(getattr(repo, "repo_url"))
        # Get "owner" and "repo" components from this repository's URL
        repo_url_components: dict = parse_url(url=repo_url)
        # If there is no `last_mined` timestamp, then this `repo_url` has not 
        # been mined before. If so, set `last_mined` to some arbitrarily early
        # time: 
        last_mined: str = getattr(repo, "last_mined")
        if last_mined == None:
            last_mined: str = "1970-01-01T00:00:00Z"
        else:
            pass
        # Get current timestamp to record as last mined time in exported data
        # The `datetime.timezone.utc` argument tells now() to use UTC timezone
        # (or use datetime.datetime.utcnow())
        timestamp_object: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        date_now: str = str(timestamp_object.date())
        time_now: str = str(timestamp_object.time())
        timestamp_now: str = str(date_now + "T" + time_now + "Z")

        # Check remaining API quota
        check_rate_limit(token=token)

        # Get branches
        branches: list = get_branches(repo=repo_url_components, token=token)
        print(f"This repository's branches: ")
        print(branches)

        # Get commits
        commits = get_commits(repo=repo_url_components, since=last_mined, token=token)

        # Get commit file changes

        # Get issues

        # Combine results

    mined_data: pandas.core.frame.DataFrame = repo_list

    return mined_data