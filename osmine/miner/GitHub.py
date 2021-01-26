#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import datetime
import string
import sys
import time
import urllib.parse

# External imports
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
# GitHub API query response codes when retry will be attempted
RETRY_CODES: list = [429, 500, 502, 503, 504]
# Initial retry wait time in seconds
RETRY_WAIT: int = 15
# Numbers of times to retry before fail
RETRIES: int = 7
# Requested results per page for each API response
PER_PAGE: int = 100
# An arbitrarily early "last minted" timestamp if a repository has not been 
# mined before
DEFAULT_LAST_MINED: str = "1970-01-01T00:00:00.000000+00:00"

#
# Define query-making functions
#

# Define a custom exception for when queries fail repeatedly
class GitHubAPIError(Exception): 
    pass

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
        print(f"Looks like a REST query...", file=sys.stderr)
        rest_headers: dict = get_headers(api="REST", token=token)
        # query_response = http_session.get(url=query, headers=rest_headers)
        query_response: requests.models.Response = requests.get(url=query,
                                                                headers=rest_headers)
        if query_response.status_code == SUCCESS_CODE:
            return query_response
        else:
            raise GitHubAPIError(f"Problem with query with return code {query_response.status_code}.")
    # Basic potato check if query looks like GraphQL
    elif ("{" in query) and ("}" in query):
        print(f"Looks like a GraphQL query...", file=sys.stderr)
        graphql_headers: dict = get_headers(api="GraphQL", token=token)
        query_success: bool = False
        retries: int = 0
        while not query_success:
            try:
                query_response: requests.models.Response = requests.post(url=GRAPHQL_URL, 
                                                                         json={"query": query}, 
                                                                         headers=graphql_headers)
                if query_response.status_code == SUCCESS_CODE:
                    query_success = True
                    return query_response
                elif (query_response.status_code in RETRY_CODES):
                    response_code: int = query_response.status_code
                    if retries < RETRIES:
                        print(f"Status code {response_code} - Retrying in {RETRY_WAIT} seconds.", file=sys.stderr)
                        time.sleep(RETRY_WAIT)
                        retries += 1
                    else:
                        raise GitHubAPIError(f"Retried {retries} times. Problem with query with return code {query_response.status_code}.")
                else:
                    raise GitHubAPIError(f"Problem with query with return code {query_response.status_code}.")
            except ConnectionError:
                if retries < RETRIES: 
                    print(f"ConnectionError - Retrying in {RETRY_WAIT} seconds.", file=sys.stderr)
                    time.sleep(RETRY_WAIT)
                    retries += 1
                else:
                    raise GitHubAPIError(f"Retried {retries} times with ConnectionError on last try.")
            
            
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

# Get basic metadata about repository

def get_basics(repo: dict, token: str) -> dict:
    """[summary]

    Args:
        repo (dict): [description]
        token (str): [description]
    """
    query_basics_template = string.Template(
    """
    {
        repository(owner: "$owner", name: "$name") {
            createdAt
            forkCount
            licenseInfo {
                spdxId
                pseudoLicense
            }
        }
    }
    """
    )
    query_basis: str = query_basics_template.substitute(owner=repo["owner"],
                                                        name=repo["name"])
    results: dict = make_query(query=query_basis, token=token).json()["data"]["repository"]
    return results

# Get branches
def get_branches(repo: dict, token: str) -> list:
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
    query_branches_template = string.Template(
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
def get_commits_3(repo: dict, since: str, token: str) -> list:
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
    commits: list = []
    
    # Send queries as long as there are more pages of results
    # References: 
    # https://stackoverflow.com/q/17777845/186904
    # https://stackoverflow.com/q/56206038/186904
    # https://docs.github.com/en/free-pro-team@latest/rest/guides/traversing-with-pagination
    get_next_page: bool = True
    while get_next_page: 
        response: requests.models.Response = make_query(query=query_string, token=token)
        # See if there is a next page of results
        if not ("Link" in response.headers):
            # If there's only one page of results, then there is no "Link" item
            # in the response header, so don't go to next page and save results.
            get_next_page = False
            # Add results from this loop iteration to commits list
            commits.extend(response.json())
        elif 'rel="next"' in response.headers["Link"]:
            # If there are multiple pages of results, then there will be
            # "rel=next" in the response header "Link". So increment page
            # counter and save current result.
            page = page + 1
            query_string: str = f"{query_string}?per_page={PER_PAGE}&page={page}"
            # Add results from this loop iteration to commits list
            commits.extend(response.json())
        else: 
            # Stop if the response header's "Link" section doesn't show a 
            # next page.
            get_next_page = False
            # Add results from this loop iteration to commits list
            commits.extend(response.json())

    # Format into ForgeFed model
    
    return commits

# Get commits from GraphQL API
def get_commits_4(repo: dict, branches: list, since: str, token: str) -> list:
    """
    Use GitHub's v4 GraphQL API
    """
    # Track if there is a next page of results
    query_has_next_page: bool = True
    # Track results page number
    query_page: int = 1
    # Create a pagination cursor
    end_cursor: str = "null" # "null" because there is no cursor for first query
    # Create empty list of commits to populate from query results
    commits: list = []
    # Create a list of just commit `oid`s which are the commit SHAs
    # TODO: Include list of previously mined commit `oid`s here to prevent duplication
    commit_oids: list = []
    # Create a string template for commits query
    query_commits_template = string.Template(
    """
    {
        repository(owner: "$owner", name: "$name") {
            refs(query: "$branch", refPrefix: "refs/heads/", first: 1) {
                nodes {
                    target {
                        ... on Commit {
                            history(first: $per_page, after: $after, since: "$since_time", until: null) {
                                nodes {
                                    oid
                                    commitUrl
                                    url
                                    messageHeadline
                                    authoredByCommitter
                                    authoredDate
                                    author {
                                        name
                                        email
                                        user {
                                            email
                                            login
                                            name
                                            twitterUsername
                                        }
                                        date
                                    }
                                    committedDate
                                    committer {
                                        name
                                        email
                                        user {
                                            email
                                            login
                                            name
                                            twitterUsername
                                        }
                                        date
                                    }
                                    parents(first: 100) {
                                        nodes {
                                            oid
                                        }
                                        pageInfo {
                                            hasNextPage
                                        endCursor
                                        }
                                    }
                                    changedFiles
                                    $tree
                                }
                                pageInfo {
                                    hasNextPage
                                    endCursor
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    )
    print(f"Getting commits after {since}", file=sys.stderr)
    # Create a string for `$tree` in the search query. This is based on the
    # recursive depth to search for/list changed files in a commit determined
    # by `COMMIT_FILE_DEPTH` (TODO: Implement this).
    tree_depth: str = """
                                tree {
                                    entries {
                                        name
                                    }
                                }
    """

    # Start by looping through each branch
    for branch in branches:
        print(f"Getting commits for the branch: {branch}", file=sys.stderr)
        # Within each branch, get as many pages as needed of its commits
        while query_has_next_page:
            print(f"    Getting page {query_page} of commits list", file=sys.stderr)
            # Prepare and execute GraphQL query for commits
            query_commits = query_commits_template.substitute(owner=repo["owner"],
                                                              name=repo["name"],
                                                              branch=branch,
                                                              per_page=PER_PAGE,
                                                              after=end_cursor,
                                                              since_time=since,
                                                              tree=tree_depth)
            results = make_query(query_commits, token=token).json()["data"]["repository"]["refs"]["nodes"][0]["target"]["history"]
            # Add newly-encountered commits to list
            for c in results["nodes"]:
                # For some reason, sometimes the results include empty items, 
                # skip them for now.
                if c == None: 
                    pass
                # Only add a commit to list if its not already known
                elif c["oid"] not in commit_oids:
                    commit_oids.append(c["oid"])
                    # Append relevant commit metadata to known commits list
                    commit = {"oid": c["oid"],
                              "commit_url": c["commitUrl"],
                              "commit_message_headline": c["messageHeadline"],
                              "committer_user": "", # Handle immediately below
                              "committer_email": "", # Handle immediately below
                              "commit_date": c["authoredDate"],
                              "parent_oids": [],
                              "changed_files": c["changedFiles"],
                              "file_list": []}
                    # Handle edge case when committer is "GitHub"
                    if "GitHub" in c["author"]["name"]:
                        commit["committer_user"] = "GitHub"
                        commit["committer_email"] = c["author"]["email"]
                    # Handle edge case when committer doesn't have `user` name/login
                    # (presumably this committer doesn't have a GitHub account?
                    # TODO: ask on GitHub Community forums with example: 
                    # https://github.com/Safecast/bGeigieNanoKit/commit/a50c2374d4acd962621d25b5159c8f82d7e8db6a)
                    elif c["author"]["user"] is None:
                        commit["committer_user"] = c["author"]["name"]
                        commit["committer_email"] = c["author"]["email"]
                    else:
                        commit["committer_user"] = c["author"]["user"]["login"]
                        commit["committer_email"] = c["author"]["email"]
                    # Append parent commit(s) oid(s) to a list in commit object
                    for parent in c["parents"]["nodes"]:
                        commit["parent_oids"].append(parent["oid"])
                    # Append changed file(s) names to a list in commit object
                    # TODO: This needs to be expanded once there's more depth here.
                    for f in c["tree"]["entries"]:
                        commit["file_list"].append(f["name"])
                    commits.append(commit)
            # See if there are more pages to retrieve, if so will loop again
            query_has_next_page = results["pageInfo"]["hasNextPage"]
            if query_has_next_page:
                # Get end cursor of current page so next loop will know where to start
                end_cursor = results["pageInfo"]["endCursor"]
                end_cursor = f'"{end_cursor}"' # Add extra quotes to form correct query
                query_page = query_page + 1
        # Reset for loop counters for next branch/iteration
        query_has_next_page = True
        query_page = 1
        end_cursor = "null"

    # Print total number of commits
    print(f"Total commits mined from {repo['owner']}/{repo['name']}: {len(commit_oids)}", file=sys.stderr)

    # Reorganise commits for this function to return in ForgeFed format
    formatted_commits: list = []
    for commit in commits:
        commit_data: dict = {
            "committedBy": commit["committer_user"],
            "committed": commit["commit_date"],
            "hash": commit["oid"],
            "summary": commit["commit_message_headline"],
            "parents": commit["parent_oids"],
            "url": commit["commit_url"]
        }
        formatted_commits.append(commit_data)
    return formatted_commits

# Get commit file changes
def get_file_changes():
    """
    Right now, this will need to use the REST API for *each* commit!
    """
    # Fetch data

    # Format into ForgeFed model
    
    pass

# Get issues
def get_issues(repo: dict, since: str, token: str) -> list:
    """
    Use GraphQL API
    """
    # Fetch data

    # Track if there is a next page of results
    query_has_next_page: bool = True
    # Track results page number
    query_page: int = 1
    # Create a pagination cursor
    end_cursor: str = "null" # "null" because there is no cursor for first query
    # Initialise an empty list of issues
    issues: list = []
    # Create a string template for issues query
    query_issues_template = string.Template(
    """
    {
        repository(owner: "$owner", name: "$name") {
            issues(first: $per_page, after: $after, filterBy: {since: "$since_time"}, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    number
                    title
                    author {
                        login
                    }
                    participants(first: $per_page) {
                        nodes {
                            name
                            login
                            email
                            twitterUsername
                            url
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                    url
                    createdAt
                    closed
                    closedAt
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
    # Create string template for issue participants query in case there are more than
    # 100 participants in an issue which would need another page of results
    query_participants_template = string.Template(
    """
    {
        repository(owner: "$owner", name: "$name") {
            issue(number: $number) {
                participants(first: $per_page, after: $after) {
                    nodes {
                        name
                        login
                        email
                        twitterUsername
                        url
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    }
    """
    )

    print(f"Retrieving {repo['owner']}/{repo['name']}'s issues metadata after {since}", file=sys.stderr)

    while query_has_next_page:
        print(f"    Getting page {query_page} of issues")
        # Prepare and execute GraphQL query for commits
        query_issues = query_issues_template.substitute(owner=repo["owner"],
                                                        name=repo["name"],
                                                        per_page=PER_PAGE,
                                                        after=end_cursor,
                                                        since_time=since)
        results = make_query(query_issues, token=token).json()["data"]["repository"]["issues"]
        # Add newly-encountered issues to list
        for i in results["nodes"]:
            issue = {"number": i["number"],
                    "title": i["title"],
                    "author": i["author"]["login"],
                    "participants": i["participants"]["nodes"],
                    "url": i["url"],
                    "createdAt": i["createdAt"],
                    "closed": i["closed"],
                    "closedAt": i["closedAt"]}
            # Paginate through list of participants and add more as needed
            participants_has_next_page: bool = i["participants"]["pageInfo"]["hasNextPage"]
            participants_page: int = 2
            participants_end_cursor: str = f"{i['participants']['pageInfo']['endCursor']}"
            participants_end_cursor = f'"{participants_end_cursor}"'
            issue_number: int = i["number"]
            while participants_has_next_page:
                
                print(f"        Getting page {participants_page} of participants list in issue {issue_number}", file=sys.tderr)
                query_participants = query_participants_template.substitute(owner=repo["owner"],
                                                                            name=repo["name"],
                                                                            number=i["number"],
                                                                            per_page=PER_PAGE,
                                                                            after=participants_end_cursor)
                participants_results = make_query(query_participants, token=token).json()["data"]["repository"]["issue"]["participants"]
                # Add each participant to existing list
                for p in participants_results["nodes"]:
                    issue["participants"].append(p)
                participants_has_next_page = participants_results["pageInfo"]["hasNextPage"]
                participants_end_cursor = participants_results['pageInfo']['endCursor']
                participants_end_cursor = f'"{participants_end_cursor}"' # Add extra quotes to form correct query
                participants_page += 1
            # Finally, add this issue to list
            issues.append(issue)
        # Prepare for next iteration of loop if there's another page of issues
        query_has_next_page = results["pageInfo"]["hasNextPage"]
        if query_has_next_page:
            end_cursor = results["pageInfo"]["endCursor"]
            end_cursor = f'"{end_cursor}"' # Add extra quotes to form correct query
            query_page += 1

    # Just to have a breakpoint
    print("Finished getting issues", file=sys.stderr)

    # Reorganise commits for this function to return in ForgeFed format
    formatted_issues: list = []
    for issue in issues:
        issue_data: dict = {
            "attributedTo": issue["author"],
            "summary": issue["title"],
            "published": issue["createdAt"],
            "isResolved": issue["closed"],
            "resolved": issue["closedAt"],
            "id": issue["number"],
            "participants": [],
            "url": issue["url"]
        }
        for participant in issue["participants"]:
            issue_data["participants"].append(participant["login"])
        formatted_issues.append(issue_data)
    
    return formatted_issues

#
# Main logic for making GitHub queries
#

def GitHub(repos: list, token: str) -> list:
    """
    docstring
    """
    print(f"Begin GitHub adapter", file=sys.stderr)

    # Initialise empty list to hold mined data where each item is a repository
    # mined_repos: list = []

    # For each repository in staged data, mine data at its URL based on last-
    # mined timestamp.
    for repo in repos: 
        # Track if there has been an API query error for this repository
        mining_error: bool = False
        print(f"Processing: " + repo["Repository"]["repo_url"], file=sys.stderr)
        repo_url: str = repo["Repository"]["repo_url"]
        # Get "owner" and "repo" components from this repository's URL
        repo_url_components: dict = parse_url(url=repo_url)
        
        last_mined: str = repo["Repository"]["last_mined"]
        # Get current timestamp to record as last mined time in exported data
        # The `datetime.timezone.utc` argument tells `now()` to use UTC 
        # timezone (or use `datetime.datetime.utcnow()`)
        timestamp_object: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        date_now: str = str(timestamp_object.date())
        time_now: str = str(timestamp_object.time())
        timestamp_now: str = str(date_now + "T" + time_now + "Z")

        # If there is no `last_mined` timestamp, then this `repo_url` has not 
        # been mined before. If so, set `last_mined` to some arbitrarily early
        # time: 
        if repo["Repository"]["last_mined"] == "": 
            last_mined: str = DEFAULT_LAST_MINED
        else:
            last_mined: str = repo["Repository"]["last_mined"]

        # Check remaining API quota
        # TODO: Raise custom exception if insufficient quota?
        check_rate_limit(token=token)

        # Get basic information
        if mining_error == False: 
            try:
                basics: dict = get_basics(repo=repo_url_components, token=token)
            except GitHubAPIError:
                print(f"There has been an error with querying this repository.", file=sys.stderr)
                mining_error = True
        else: 
            pass

        # Get branches
        if mining_error == False:
            try:
                branches: list = get_branches(repo=repo_url_components, token=token)
                print(f"This repository's branches: ", file=sys.stderr)
                print(branches, file=sys.stderr)
                repo["Branches"] = branches
            except GitHubAPIError:
                print(f"There has been an error querying this repository's branches.", file=sys.stderr)
                mining_error = True
        else:
            pass

        # Get commits
        if mining_error == False: 
            try:
                commits: list = get_commits_4(repo=repo_url_components, branches=repo["Branches"], since=last_mined, token=token)
                repo["Commits"].extend(commits)
            except GitHubAPIError:
                print(f"There has been an error querying this repository's commits.", file=sys.stderr)
                mining_error = True
        else: 
            pass

        # Get issues
        if mining_error == False: 
            try: 
                issues: list = get_issues(repo=repo_url_components, since=last_mined, token=token)
                repo["Tickets"].extend(issues)
            except GitHubAPIError: 
                print(f"There has been an error querying issues in this repository.")
                mining_error = True
        else:
            pass
        
        if mining_error == False: 
            # Record basic repository metadata
            mined_repo: dict = {}
            mined_repo["Repository"] = {
                "name": repo_url_components["name"], 
                "attributedTo": repo_url_components["owner"],
                "published": basics["createdAt"],
                "project": repo["Repository"]["project"],
                "forkcount": basics["forkCount"],
                "forks": [],
                "license": "",
                "platform": "GitHub",
                "repo_url": repo_url,
                "last_mined": timestamp_now
                }
            if basics["licenseInfo"] is None:
                mined_repo["Repository"]["license"] = "no-LICENSE"
            elif basics["licenseInfo"]["pseudoLicense"]:
                mined_repo["Repository"]["license"] = "other"
            else:
                mined_repo["Repository"]["license"] = basics["licenseInfo"]["spdxId"]
            repo["Repository"] = mined_repo["Repository"]
        else: 
            pass

    return repos