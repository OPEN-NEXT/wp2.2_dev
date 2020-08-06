#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# This script is an initial exploration of using GitHub's version 4 GraphQL
# API to fetch the commit history of a given repository and construct a 
# viewable GraphML visualisation.
#
# The goal is to eventually incorporate this into the next generation data
# mining script for open source hardware repositories hosted on GitHub.

# DONE: Produce at least a Git history graph from commits data
# TODO: Allow specifying time window for queries.
# DONE: Check rate limit before running and raise Warnings and Errors as needed
# TODO: Implement identity management
# DONE: Replace gql library with built-in requests library
# DONE: Retrieve files changed for each commit via GitHub REST API
# TODO: Use the built-in `asyncio` library to speed up requests

import json
import sys
from string import Template
from sys import stderr
import itertools

import networkx
import requests

"""

Set basic parameters for this script

"""

# GitHub API GraphQL API endpoint
GITHUB_API_URL: str = "https://api.github.com/graphql"
# Path to GitHub API authorisation token file
TOKEN_PATH: str = "token"
# GitHub repository's owner
GITHUB_REPO_OWNER: str = "OPEN-NEXT"
# GitHub repository's name
GITHUB_REPO_NAME: str = "wp2.2_dev"

"""

Read GitHub API token

"""


# Read GitHub authorisation token from file
try:
    with open(TOKEN_PATH, mode="r") as token_file:
        token_file_lines = token_file.read().split(sep="\n")
        # Read first line of provided token file as authentication token string
        auth_token = token_file_lines[0]
    del token_file, token_file_lines
except FileNotFoundError as token_file_error:
    print(f"Can't find GitHub API authentication token file.", file=stderr)
    sys.exit(1)
except Exception as other_error:
    print(f"Error accessing GitHub API authentication token file: {other_error}", file=stderr)
    sys.exit(1)
else: 
    # Check if authentication key string looks correct
    # AFAIK the token should be exactly 40 alphanumeric characters
    try:
        assert (auth_token.isalnum() and len(auth_token) == 40)
    except AssertionError:
        print("GitHub authentication key doesn't look right: {}".format(auth_token), file=stderr)
        print("It should be a 40-character alphanumeric string. Please try again.", file=stderr)
        sys.exit(1)
    else:
        print("GitHub authentication key looks OK.", file=stderr)


"""

Prepare query-related functions & parameters

"""


# Set up GitHub v3 API REST request headers
rest_headers: dict = {"Accept": "application/vnd.github.v3+json",
                      "Authorization": f"token {auth_token}"}
# Set up GitHub v4 API GraphQL request headers
graphql_headers: dict = {"Authorization": f"token {auth_token}"}

# Declare a function for GraphQL queries
def graphql_query(query: str):
    request = requests.post(url=GITHUB_API_URL, json={"query": query}, headers=graphql_headers)
    if request.status_code == 200:
        return request.json()["data"]
    else:
        raise Exception(f"Problem with query with return code {request.status_code}.")

# Check rate limits
def check_rate_limit():
    query_rate_limit = """
    {
        rateLimit {
            remaining
            resetAt
        }
    }
    """
    results = graphql_query(query_rate_limit)["rateLimit"]
    remaining = results["remaining"]
    resetAt = results["resetAt"]
    print(f"GitHub API queries remaining: {remaining}", file=stderr)
    print(f"    Quota will reset at: {resetAt}", file=stderr)
    try:
        assert results["remaining"] >= 1000
    except AssertionError:
        print(f"Warning: Only {remaining} queries remaining", file=stderr)


check_rate_limit()

"""

Query for repository's branches

"""

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
    refs(first: 100, refPrefix: "refs/heads/", after: $after) {
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
    print(f"Getting page {query_page} of branches list", file=stderr)
    # Prepare and execute GraphQL query
    query_branches = query_branches_template.substitute(owner=GITHUB_REPO_OWNER, 
                                                        name=GITHUB_REPO_NAME, 
                                                        after=end_cursor)
    results = graphql_query(query_branches)["repository"]["refs"]
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
print(f"Number of branches: {len(branches)}", file=stderr)

"""

Query for commits using branches information

"""

# Track if there is a next page of results
query_has_next_page: bool = True
# Track results page number
query_page: int = 1
# Create a pagination cursor
end_cursor: str = "null" # "null" because there is no cursor for first query
# Create empty list of commits to populate from query results
commits: list = []
# Create a list of just commit `oid`s
commit_oids: list = []
# Create a string template for commits query
query_commits_template = Template(
"""
{
  repository(owner: "$owner", name: "$name") {
    refs(query: "$branch", refPrefix: "refs/heads/", first: 1) {
      nodes {
        target {
          ... on Commit {
            history(first: 100, after: $after, since: null, until: null) {
              nodes {
                oid
                commitUrl
                url
                messageHeadline
                changedFiles
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

# Start by looping through each branch
for branch in branches:
    print(f"Getting commits for the branch: {branch}", file=stderr)
    # Within each branch, get as many pages as needed of its commits
    while query_has_next_page:
        print(f"    Getting page {query_page} of commits list", file=stderr)
        # Prepare and execute GraphQL query for commits
        query_commits = query_commits_template.substitute(owner=GITHUB_REPO_OWNER,
                                                          name=GITHUB_REPO_NAME,
                                                          branch=branch,
                                                          after=end_cursor)
        results = graphql_query(query_commits)["repository"]["refs"]["nodes"][0]["target"]["history"]
        # Add newly-encountered commits to list
        for c in results["nodes"]:
            # Only add a commit to list if its not already known
            if c["oid"] not in commit_oids:
                commit_oids.append(c["oid"])
                # Append relevant commit metadata to known commits list
                commit = {"oid": c["oid"],
                        "commit_url": c["commitUrl"],
                        "commit_message_headline": c["messageHeadline"],
                        "committer_name": c["committer"]["name"],
                        "committer_email": c["committer"]["email"],
                        "commit_date": c["committedDate"],
                        "parent_oids": [],
                        "changed_files": c["changedFiles"],
                        "file_list": []}
                # Append parent commit(s) oid(s) to a list in commit object
                for parent in c["parents"]["nodes"]:
                    commit["parent_oids"].append(parent["oid"])
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
print(f"Total commits in repository {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}: {len(commit_oids)}",
      file=stderr)


"""

Retrieve file change metadata for commits

"""

# According to the following post, the GitHub GraphQL API does not support retrieving 
# a commit's list of changed files, so we will need to use the REST API for now:
# https://github.community/t/graphql-api-get-list-of-files-related-to-commit/14047

# Set up a counter to track progress
query_counter: int = 0
# Go through each commit and retrieve its list of changed files
print("Retrieving file change list for each commit...", file=stderr)
#n_commits: int = len(commits)
for i in range(len(commits)):
    commit_oid: str = commits[i]["oid"]
    rest_request_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits/{commit_oid}"
    results = requests.get(url=rest_request_url,
                           headers=rest_headers).json()
    file_list: list = results["files"]
    try:
        # The number of files from REST API should equal that from the GraphQL API
        assert len(file_list) == commits[i]["changed_files"]
    except AssertionError:
        # If not, raise warning (maybe error and exit?)
        warning_message = f"Commit {commit_oid}'s changed files are not all accounted for."
        raise Warning(warning_message)
    else:
        # Add changed files list to commit history
        commits[i]["file_list"] = file_list
    
    # Regularly update on queries' progress
    if query_counter%20 == 0:
        # This progress indicator is just a first draft
        print(f"Progress: {query_counter}/{len(commits)} commits processed", file=stderr)
    query_counter += 1

"""

Produce Git commit history graph

"""

# Initialise an empty NetworkX directed graph
commit_history_graph = networkx.DiGraph(name=f"{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME} commit history")

# Add each commit as a node
commit_history_graph.add_nodes_from(commit_oids)

for commit in commits:
    # Add commit metadata to corresponding node's attributes
    for key in commit.keys():
        # NetworkX GraphML export doesn't support lists as attributes
        # so skip those (e.g. "parent_oids") for now
        if isinstance(commit[key], list):
            # TODO: Add log entry here.
            pass
            #print(f"{key} is a list which is unsupported when exporting to GraphML.", file=stderr)
        else:
            # Append all other attributes
            commit_history_graph.nodes[commit["oid"]][key] = commit[key]            
    # Add directed edges with parentage metadata of each commit
    # Only process commits with at least one parent
    if len(commit["parent_oids"]) > 0:
        # Go through each parent and add edge to graph
        for parent_oid in commit["parent_oids"]:
            commit_history_graph.add_edge(commit["oid"], parent_oid)

# Export GraphML
output_filename: str = f"{GITHUB_REPO_OWNER}-{GITHUB_REPO_NAME}_commit_history.GraphML"
networkx.write_graphml(commit_history_graph, output_filename)

# Export visjs visualisation
# load the visjs template into a string
with open('visjs_template.html', 'r') as f:
    html_string = f.read()
# generate a string with js code including networkx data to concatenate with the visjs template
js_string = []
js_string.append("<script type='text/javascript'>\r\n")
js_string.append("imported_data = ")
js_string.append(json.dumps(networkx.node_link_data(commit_history_graph), sort_keys=True, indent=4))
js_string.append("\r\n</script>\r\n")
# Export HTML file
with open(f"{GITHUB_REPO_OWNER}-{GITHUB_REPO_NAME}_commit_history.html", 'w') as f:
    f.write(''.join(js_string) + html_string)
del f

"""

Fetch GitHub repository's issues and participants

"""

# Track if there is a next page of results
query_has_next_page: bool = True
# Track results page number
query_page: int = 1
# Create a pagination cursor
end_cursor: str = "null" # "null" because there is no cursor for first query
# Initialise an empty list of issues
issues: list = []
# Create a string template for issues query
query_issues_template = Template(
"""
{
  repository(owner: "$owner", name: "$name") {
    issues(first: 100, after: $after, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        number
        title
        author {
          login
        }
        participants(first: 100) {
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
query_participants_template = Template(
"""
{
  repository(owner: "$owner", name: "$name") {
    issue(number: $number) {
      participants(first: 100, after: $after) {
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

print(f"Retrieving {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}'s issues metadata...", file=stderr)

while query_has_next_page:
    print(f"    Getting page {query_page} of issues")
    # Prepare and execute GraphQL query for commits
    query_issues = query_issues_template.substitute(owner=GITHUB_REPO_OWNER,
                                                      name=GITHUB_REPO_NAME,
                                                      after=end_cursor)
    results = graphql_query(query_issues)["repository"]["issues"]
    # Add newly-encountered issues to list
    for i in results["nodes"]:
        issue = {"number": i["number"],
                 "title": i["title"],
                 "author": i["author"]["login"],
                 "participants": i["participants"]["nodes"],
                 "url": i["url"]}
        # Paginate through list of participants and add more as needed
        participants_has_next_page: bool = i["participants"]["pageInfo"]["hasNextPage"]
        participants_page: int = 2
        participants_end_cursor: str = f"{i['participants']['pageInfo']['endCursor']}"
        participants_end_cursor = f'"{participants_end_cursor}"'
        issue_number: int = i["number"]
        while participants_has_next_page:
            
            print(f"        Getting page {participants_page} of participants list in issue {issue_number}", file=stderr)
            query_participants = query_participants_template.substitute(owner=GITHUB_REPO_OWNER,
                                                                        name=GITHUB_REPO_NAME,
                                                                        number=i["number"],
                                                                        after=participants_end_cursor)
            participants_results = graphql_query(query_participants)["repository"]["issue"]["participants"]
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