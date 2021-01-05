#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import json
import os
import sys
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
        request = requests.get(url=query,
                               headers=rest_headers).json()
    # Basic potato check if query looks like GraphQL
    elif ("{" in query) and ("}" in query):
        print(f"Looks like a GraphQL query...")
        graphql_headers: dict = get_headers(api="GraphQL", token=token)
        request = requests.post(url=GRAPHQL_URL, json={"query": query}, headers=graphql_headers)
        if request.status_code == SUCCESS_CODE:
            return request.json()["data"]
        else:
            raise Exception(f"Problem with query with return code {request.status_code}.")
    else:
        print(f"ERROR: Query does not look like REST or GraphQL...", file=sys.stderr)

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
    results = make_query(query=query_rate_limit, token=token)["rateLimit"]
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
def get_branches():
    """
    Use GraphQL API
    """
    # Fetch data

    # Format into ForgeFed model

    pass

# Get commits
def get_commits():
    """
    Use REST API
    """
    # Fetch data

    # Format into ForgeFed model
    
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
        print(token)
        # If there is no `last_mined` timestamp, then this `repo_url` has not 
        # been mined before. If so, set `last_mined` to some arbitrarily early
        # time: 
        last_mined: str = getattr(repo, "last_mined")
        if last_mined == None:
            last_mined: str = "1970-01-01T00:00:00.0+00:00"
        else:
            pass

    mined_data: pandas.core.frame.DataFrame = repo_list

    return mined_data