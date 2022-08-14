#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import os
import string
import sys
import urllib

# External imports
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import requests

# Internal imports
import oshminer.filetypes as filetypes
from oshminer.errors import exceptions

# GitHub GraphQL API URL
GITHUB_GRAPHQL_URL: str = "https://api.github.com/graphql"
# GitHub REST API URL
GITHUB_REST_URL: str = "https://api.github.com"
# GitHub API query success response code
SUCCESS_CODE: int = 200
# GitHub API query response codes when retry will be attempted
RETRY_CODES: list = [429, 500, 502, 503, 504]
# Initial retry wait time in seconds
RETRY_WAIT: int = 10
# Numbers of times to retry before fail
RETRIES: int = 3
# Requested results per page for each API response
PER_PAGE: int = 100
# Get GitHub API personal access token from environment variable
GITHUB_API_TOKEN: str = os.environ.get("GITHUB_TOKEN")

#
# Helper functions
#

# Parse GitHub repository URL to get its "owner" and "name" components
def parse_url(url: str) -> dict:
    """
    For example, given `url="https://github.com/octocat/Hello-World/"`, it 
    would be parsed by `urllib.parse.urlparse()` into components, of which the
    path component can be split into the "owner" and "name", i.e. "octocat" and
    "Hello-World".
    """
    parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    parsed_repo: dict = {
        # Get the path component of a `urlparse()`ed URL which looks like
        # "/octocat/Hello-World", then split it by "/" where first part would 
        # be "owner", second part would be "name". 
        # E.g. https://github.com/octocat/Hello-World would have owner 
        # "octocat" and name "Hello-World".
        "owner": getattr(parsed_url, "path").split(sep="/")[1],
        "name": getattr(parsed_url, "path").split(sep="/")[2]
    }
    return parsed_repo

# Get full file list of GitHub repository on default branch
async def get_file_list(project: dict, session) -> list: 
    """
    Use GitHub v3 REST API to make a recursive request for the repository's
    `tree` on the default branch. This gives the full file list.
    """
    #
    # Determine name of default branch
    #
    
    # This can be done with GitHub v4 GraphQL API
    query_default_branch = gql(
        """
        query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                defaultBranchRef {
                    name
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "owner": project["owner"], 
        "name": project["name"]
    }
    # Execute query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    try: 
        query_default_branch_response: dict = await session.execute(query_default_branch, variable_values = params)
    except Exception as exc: 
        # Very hacky workaround for now: 
        # When there's an authorisation error such as a bad personal access token, 
        # GitHub would return a 401 error response. The `gql` library woudl throw the 
        # `gql.transport.exceptions.TransportServerError` exception.
        # But for some reason `except gql.transport.exceptions.TransportServerError`
        # would fail, so for now I'm manually catching the 401 code here.
        if exc.code == 401: 
            raise exceptions.BadGitHubTokenError()
        else: 
            # For all other errors, continue throwing an exception to stop execution.
            raise Exception
    default_branch_name: str = query_default_branch_response["repository"]["defaultBranchRef"]["name"]
    
    #
    # Request repository tree on default branch
    #
    
    # Create query via repository tree, see: 
    # https://stackoverflow.com/q/25022016/186904
    owner: str = project["owner"]
    name: str = project["name"]
    query_repo_tree: str = f"{GITHUB_REST_URL}/repos/{owner}/{name}/git/trees/{default_branch_name}?recursive=1"
    # Make query
    query_repo_tree_response: requests.models.Response = requests.get(
        url = query_repo_tree, 
        headers = {
            "Accept": "application/vnd.github.v3+json", 
            "Authorization": f"bearer {GITHUB_API_TOKEN}"
            }
    )
    # Get flat list of files from query response
    repo_tree: list = query_repo_tree_response.json()["tree"]
    # Items of type "blob" are files in the tree
    # Note: List comprehension instead of `filter()` is even faster: 
    # https://stackoverflow.com/a/69623735/186904
    repo_blobs: list = list(filter(lambda b: b["type"] == "blob", repo_tree))
    # Get just the path from each blob
    paths_list: list = [p["path"] for p in repo_blobs]
    # The last part of a path is the filename, keep that
    file_list: list = [f.split("/")[-1] for f in paths_list]
    
    return file_list

#
# Implement requestable information
#

async def get_files_editability(project: dict, session) -> dict: 
    """
    Return a `dict` of files in this repository and an assessment of their 
    editability based on the `osh-file-types` lists from: 
    https://gitlab.com/OSEGermany/osh-file-types/
    
    Based on the file list of the repository on its default branch.
    """
    
    # Get complete file list of the repository
    file_list: list = await get_file_list(project, session)
    
    # Derive extensions from file list
    filenames: list = [{"filename": f, "extension": f.split(".")[-1].lower()} for f in file_list]
    # Get a list of files that are not documents (e.g. .md) or data. What's left
    # should be mostly CAD files.
    cad_filenames: list = [c for c in filenames if c["extension"] not in filetypes.data and c["extension"] not in filetypes.document]
    
    # Get lists of open/closed file extensions   
    open_file_extensions: list = [o["extension"] for o in filetypes.osh_file_types if o["format"] == "open"]
    closed_file_extensions: list = [o["extension"] for o in filetypes.osh_file_types if o["format"] == "proprietary"]
    # Get lists of binary and text file extensions
    binary_file_extensions: list = [o["extension"] for o in filetypes.osh_file_types if o["encoding"] == "binary"]
    text_file_extensions: list = [o["extension"] for o in filetypes.osh_file_types if o["encoding"] == "text"]
    
    # Count number of files in repository that are open, closed, and other
    cad_files_openness: dict = {
        "open": len([f for f in cad_filenames if f["extension"] in open_file_extensions]), 
        "closed": len([f for f in cad_filenames if f["extension"] in closed_file_extensions])
    }
    cad_files_openness["other"]: int = len(cad_filenames) - cad_files_openness["open"] - cad_files_openness["closed"]
    
    # Count number of files in repository that are binary, text, and other
    cad_files_encoding: dict = {
        "binary": len([f for f in cad_filenames if f["extension"] in binary_file_extensions]), 
        "text": len([f for f in cad_filenames if f["extension"] in text_file_extensions])
    }
    cad_files_encoding["other"]: int = len(cad_filenames) - cad_files_encoding["binary"] - cad_files_encoding["text"]
    
    cad_files_count: int = len(cad_filenames)
    
    # Placeholder result
    result: dict = {
        "files_editability": {
            "files_count": cad_files_count, 
            "files_openness": cad_files_openness, 
            "files_encoding": cad_files_encoding
        }
    }

    return result

async def get_files_info(project: dict, session) -> dict: 
    """
    Return a breakdown of number of files for each file types and their 
    proportions in a GitHub repository.
    """
    # Get complete file list
    file_list: list = await get_file_list(project, session)
    
    # Get file extensions
    filenames: list = [{"filename": f, "extension": f.split(".")[-1].lower()} for f in file_list]
    
    #
    # Get number and proportion of each file type
    #
    
    # Get numbers of each type
    result: dict = {
        "files_info": {
            # Total number of files
            "total_files": len(file_list),
            # Number of electronic CAD files
            "ecad_files": len([f["extension"] for f in filenames if f["extension"] in filetypes.ecad]),
            # Number of mechanical CAD files 
            "mcad_files": len([f["extension"] for f in filenames if f["extension"] in filetypes.mcad]),
            # Number of image files
            "image_files": len([f["extension"] for f in filenames if f["extension"] in filetypes.image]), 
            # Number of data files
            "data_files": len([f["extension"] for f in filenames if f["extension"] in filetypes.data]),
            # Number of document files
            "document_files": len([f["extension"] for f in filenames if f["extension"] in filetypes.document])
        }
    }
    # A `LICENSE` file often doesn't have an extension, count the number of 
    # files with this name towards `document_files`.
    license_files: int = len([f for f in file_list if f == "LICENSE"])
    result["files_info"]["document_files"] += license_files
    # Any files not matching the defined types count towards `other_files`
    result["files_info"]["other_files"]: int = result["files_info"]["total_files"]\
        - result["files_info"]["ecad_files"]\
        - result["files_info"]["mcad_files"]\
        - result["files_info"]["image_files"]\
        - result["files_info"]["data_files"]\
        - result["files_info"]["document_files"]
    # Calculate proportion of each file type
    # Limit to three decimal places to reduce size of response
    ecad_proportion: float = result["files_info"]["ecad_files"]/result["files_info"]["total_files"]
    mcad_proportion: float = result["files_info"]["mcad_files"]/result["files_info"]["total_files"]
    image_proportion: float = result["files_info"]["image_files"]/result["files_info"]["total_files"]
    data_proportion: float = result["files_info"]["data_files"]/result["files_info"]["total_files"]
    document_proportion: float = result["files_info"]["document_files"]/result["files_info"]["total_files"]
    other_proportion: float = result["files_info"]["other_files"]/result["files_info"]["total_files"]
    result["files_info"]["ecad_proportion"]: float = float(f"{ecad_proportion:.3f}")
    result["files_info"]["mcad_proportion"]: float = float(f"{mcad_proportion:.3f}")
    result["files_info"]["image_proportion"]: float = float(f"{image_proportion:.3f}")
    result["files_info"]["data_proportion"]: float = float(f"{data_proportion:.3f}")
    result["files_info"]["document_proportion"]: float = float(f"{document_proportion:.3f}")
    result["files_info"]["other_proportion"]: float = float(f"{other_proportion:.3f}")
    
    return result
    
async def get_issues_level(project: dict, session) -> dict: 
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
            issues(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
                nodes {
                    number
                    title
                    createdAt
                    updatedAt
                    url
                    state
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

    print(f"{project['name']}: Retrieving issues metadata...", file=sys.stderr)

    while query_has_next_page:
        print(f"    {project['name']}: Getting page {query_page} of issues")
        # Prepare and execute GraphQL query for issues
        query_issues = query_issues_template.substitute(owner=project["owner"],
                                                        name=project["name"],
                                                        after=end_cursor)
        # results = make_query(
        #     query_issues, 
        #     token=token
        # ).json()["data"]["repository"]["issues"]
        query_response = requests.post(
            url = GITHUB_GRAPHQL_URL, 
            json = {
                "query": query_issues
                }, 
            headers = {
                "Authorization": f"bearer {GITHUB_API_TOKEN}"
                }
        )
        query_results = query_response.json()["data"]["repository"]["issues"]
        # Add newly-encountered issues to list
        issues = issues + (query_results["nodes"])
        # Prepare for next iteration of loop if there's another page of issues
        query_has_next_page = query_results["pageInfo"]["hasNextPage"]
        if query_has_next_page:
            end_cursor = query_results["pageInfo"]["endCursor"]
            end_cursor = f'"{end_cursor}"' # Add extra quotes to form correct query
            query_page += 1

    print(f"{project['name']}: Finished getting {len(issues)} issues.", file=sys.stderr)
    
    result: dict = {
        "issues_level": issues
    }
    return result

async def get_commits_level(project: dict, session) -> dict: 
    """
    Returns a `list` of commits.
    
    Each commit is a `dict` containing as `str`s: `oid`, `messageHeadline`, 
    `committedDate`, and `url`.
    
    The commits are aggregated and de-duplicated across branches up to 3
    branches including the default branch. The 3 branch limit is because 
    otherwise the requests would take too long.
    """
    
    # 
    # Get list of branches first
    # 
    
    branches_list: list = []
    
    query_branches_template = string.Template(
    """
    {
        repository(owner: "$owner", name: "$name") {
            refs(first: 100, refPrefix: "refs/heads/") {
                nodes {
                        name
                    }
                }
            }
    }
    """
    )
    # Query variables
    params: dict = {
        "owner": project["owner"], 
        "name": project["name"]
    }
    repo_name: str = project["name"]
    # Prepare and execute GraphQL query
    query_branches: str = query_branches_template.substitute(owner=params["owner"], 
                                                        name=params["name"]) 
    # Note: I'm using the non-async `requests` library for this because I need
    # to have the list of branches *before* the next step, i.e. get commits 
    # from each branch.
    branches_response = requests.post(
        url = GITHUB_GRAPHQL_URL, 
        json = {
            "query": query_branches}, 
        headers = {
            "Authorization": f"bearer {GITHUB_API_TOKEN}"
        }
    )
    # When there's an authorisation error such as a bad personal access token, 
    # GitHub would return a 401 error response.
    if branches_response.status_code == 401: 
        raise exceptions.BadGitHubTokenError()
    else: 
        pass
    branches_results = branches_response.json()["data"]["repository"]["refs"]["nodes"]
    # Add branches from query results to list of branches
    for node in branches_results: 
        branches_list.append(node["name"])
        
    #
    # Identify default branch name
    #
    
    #
    # Determine name of default branch
    #
    
    # This can be done with GitHub v4 GraphQL API
    query_default_branch = gql(
        """
        query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                defaultBranchRef {
                    name
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "owner": project["owner"], 
        "name": project["name"]
    }
    # Execute query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    try: 
        query_default_branch_response: dict = await session.execute(query_default_branch, variable_values = params)
    except Exception as exc: 
        # Very hacky workaround for now: 
        # When there's an authorisation error such as a bad personal access token, 
        # GitHub would return a 401 error response. The `gql` library woudl throw the 
        # `gql.transport.exceptions.TransportServerError` exception.
        # But for some reason `except gql.transport.exceptions.TransportServerError`
        # would fail, so for now I'm manually catching the 401 code here.
        if exc.code == 401: 
            raise exceptions.BadGitHubTokenError()
        else: 
            # For all other errors, continue throwing an exception to stop execution.
            raise Exception
    default_branch_name: str = query_default_branch_response["repository"]["defaultBranchRef"]["name"]
    
    #
    # Keep 3 branches including default branch
    #
    
    if len(branches_list) > 3: 
        print("Keeping 3 branches to query", file=sys.stderr)
        # Keep two branches plus default branch
        branches_list.remove(default_branch_name)
        branches_list = branches_list[:2]
        branches_list.append(default_branch_name)
    
    #
    # Get list of commits in each branch
    #
    
    # Track which commit `oid`s are already found
    commits_oids: list = []
    # Actual commits with metadata for each
    commits_list: list = []
    # Query template to get total number of commits in a branch
    query_number_of_commits_template = string.Template(
        """
        {
            repository (owner: "$owner", name: "$name") {
                ref(qualifiedName: "$branch") {
                    target {
                        ... on Commit {
                            history(since: "1970-01-01T00:00:00Z", first: 1) {
                                pageInfo {
                                    endCursor
                                }
                                totalCount
                            }
                        }
                    }
                }
            }
        }
        """
    )
    
    for branch_name in branches_list: 
        print(f"{repo_name}: Finding commits for {branch_name}...", file = sys.stderr)
        # Pagination cursors
        # Note: First page doesn't need cursor, hence "null".
        cursors_list: list = ["null"]
        # Cumulative list of commits for this branch
        commits_this_branch: list = []
        # Get total number of commits in this branch
        query_number_of_commits: str = query_number_of_commits_template.substitute(
            owner = params["owner"], 
            name = params["name"], 
            branch = branch_name
        )
        number_of_commits_response = requests.post(
            url = GITHUB_GRAPHQL_URL, 
            json = {
                "query": query_number_of_commits
            }, 
            headers = {
                "Authorization": f"bearer {GITHUB_API_TOKEN}"
            }
        )
        first_commit_oid: str = number_of_commits_response.json()["data"]["repository"]["ref"]["target"]["history"]["pageInfo"]["endCursor"]
        first_commit_oid = first_commit_oid.split(" ")[0]
        number_of_commits: int = number_of_commits_response.json()["data"]["repository"]["ref"]["target"]["history"]["totalCount"]
        print(f"{repo_name}: There are {number_of_commits} in the {branch_name} branch...", file = sys.stderr)
        # Create pagination cursors if there are more than 100 commits in this branch
        if number_of_commits > 100: 
            cursors_list.append(f'"{first_commit_oid} 99"')
            page_tracker: int = 100
            while page_tracker < number_of_commits: 
                cursors_list.append(f'"{first_commit_oid} {str(99 + page_tracker)}"')
                page_tracker += 100
            # As a result of the `while` loop, there will be an extra cursor at
            # the end, remove it.
            del cursors_list[-1]
        print(f"{repo_name}: There are {len(cursors_list)} pages of commits...")
        # Now that we have the cursors for each page, use send async requests
        # to the GitHub API to retrieve the commits from each page.
        for page_cursor in cursors_list: 
            query_commits_template = string.Template(
                """ 
                query ($owner: String!, $name: String!, $branch: String!) {
                    repository(owner: $owner, name: $name) {
                        refs(query: $branch, refPrefix: "refs/heads/", first: 100) {
                            nodes {
                                target {
                                    ... on Commit {
                                        history(first: 100, after: $cursor) {
                                            nodes {
                                                oid
                                                committedDate
                                                messageHeadline
                                                commitUrl
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
            # Use string substitution to *only* update actual $cursor, leaving 
            # the others to be handled by `gql()`.
            query_commits_template = query_commits_template.substitute(
                owner = "$owner",
                name = "$name", 
                branch = "$branch",
                cursor = page_cursor
            )
            query_commits = gql(query_commits_template)
            query_commits_variables: dict = {
                "owner": params["owner"], 
                "name": params["name"], 
                "branch": branch_name, 
                "cursor": page_cursor
            }
            commits_response: dict = await session.execute(query_commits, variable_values = query_commits_variables)
            commits_this_page: list = commits_response["repository"]["refs"]["nodes"][0]["target"]["history"]["nodes"]
            commits_this_branch = commits_this_branch + commits_this_page
        
        print(f"{repo_name}: {len(commits_this_branch)} commits have been retrieved for branch '{branch_name}'. Moving to next branch.")
        # Add commits from this branch to final list for the entire repository
        commits_list = commits_list + commits_this_branch
    
    # De-duplicate final list and return result (wam): 
    # https://www.geeksforgeeks.org/python-removing-duplicate-dicts-in-list/
    result: dict = {
        "commits_level": [i for n, i in enumerate(commits_list) if i not in commits_list[n + 1:]]
    }
    return result

async def get_tags(project: dict, session) -> dict: 
    # GraphQL query for tags ("labels" in GitHub) information
    query = gql(
        """
        query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                repositoryTopics(first: 100) {
                    nodes {
                        topic {
                            name
                        }
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
    # Query variables
    params: dict = {
        "owner": project["owner"], 
        "name": project["name"]
    }
    # Execute query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    try: 
        API_response: dict = await session.execute(query, variable_values = params)
    except Exception as exc: 
        # Very hacky workaround for now: 
        # When there's an authorisation error such as a bad personal access token, 
        # GitHub would return a 401 error response. The `gql` library woudl throw the 
        # `gql.transport.exceptions.TransportServerError` exception.
        # But for some reason `except gql.transport.exceptions.TransportServerError`
        # would fail, so for now I'm manually catching the 401 code here.
        if exc.code == 401: 
            raise exceptions.BadGitHubTokenError()
        else: 
            # For all other errors, continue throwing an exception to stop execution.
            raise Exception
    result: dict = {
        "tags": API_response["repository"]["repositoryTopics"]["nodes"]
        }
    return result

async def get_license(project: dict, session) -> dict: 
    # GraphQL query for license information
    query = gql(
        """
        query ($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                licenseInfo {
                    key
                    name
                    spdxId
                    url
                    permissions {
                        label
                    }
                    conditions {
                        label
                    }
                    limitations {
                        label
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "owner": project["owner"], 
        "name": project["name"]
    }
    # Execute query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    try: 
        API_response: dict = await session.execute(query, variable_values = params)
    except Exception as exc: 
        # Very hacky workaround for now: 
        # When there's an authorisation error such as a bad personal access token, 
        # GitHub would return a 401 error response. The `gql` library woudl throw the 
        # `gql.transport.exceptions.TransportServerError` exception.
        # But for some reason `except gql.transport.exceptions.TransportServerError`
        # would fail, so for now I'm manually catching the 401 code here.
        if exc.code == 401: 
            raise exceptions.BadGitHubTokenError()
        else: 
            # For all other errors, continue throwing an exception to stop execution.
            raise Exception
    result: dict = {
        "license": API_response["repository"]["licenseInfo"]
        }
    return result

# Map from request type to getter functions
queries: dict = {
    "files_editability": get_files_editability, 
    "files_info": get_files_info, 
    "issues_level": get_issues_level, 
    "commits_level": get_commits_level, 
    "tags": get_tags, 
    "license": get_license
}

async def make_GitHub_request(url: str, data: list) -> dict: 
    
    print(f"Constructing an API request to GitHub for repository {url} for the following data {data}", file=sys.stderr)

    # Create a dictionary to hold results from GitHub API query
    results: dict = {
        "repository": str(url), 
        "platform": "GitHub", 
        "requested_data": {}
    }
    
    # Select transport with the GitHub GraphQL API endpoint URL
    transport: AIOHTTPTransport = AIOHTTPTransport(
        url = GITHUB_GRAPHQL_URL, 
        headers = {"Authorization": f"bearer {GITHUB_API_TOKEN}"}
        )
    
    # Get "owner" and "name" of the GitHub repository
    owner_name: dict = parse_url(url)

    async with Client(transport = transport) as session:       
        for data_type in data: 
            query_result: dict = await queries[data_type](owner_name, session)
            results["requested_data"].update(query_result)
    
    return results