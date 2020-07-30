#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# This script is an initial exploration of using GitHub's version 4 GraphQL
# API to fetch the commit history of a given repository and construct a 
# viewable GraphML visualisation.
#
# The goal is to eventually incorporate this into the next generation data
# mining script for open source hardware repositories hosted on GitHub.

# TODO: Produce at least a Git history graph from commits data
# TODO: Allow specifying time window for queries.
# TODO: Check rate limit before running and raise Warnings and Errors as needed
# TODO: Implement identity management
# TODO: Consider replacing gql library with built-in requests library?????
# TODO: Retrieve files changed for each commit via GitHub REST API
# TODO: Use the built-in `asyncio` library to speed up requests

import sys
from string import Template
from sys import stderr
import json

import networkx
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

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


# Add GitHub API authorization token header
transport = RequestsHTTPTransport(url=GITHUB_API_URL, 
                                  headers={"Authorization": "token " + auth_token})

"""

Query for repository's branches

"""

client = Client(transport=transport, fetch_schema_from_transport=True)

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
query {
  repository(owner: "$owner", name: "$name") {
    refs(first: 100, refPrefix: "refs/heads/", after: $after) {
      edges {
        node {
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

while query_has_next_page:
    print(f"Getting page {query_page} of branches list", file=stderr)
    # Prepare and execute GraphQL query
    query_branches = gql(
        query_branches_template.substitute(owner=GITHUB_REPO_OWNER, 
                                           name=GITHUB_REPO_NAME,
                                           after=end_cursor)
    )
    results = client.execute(query_branches)["repository"]["refs"]
    # Get names of branches from query results and apstrpend to known branches list
    results_edges = results["edges"]
    for edge in results_edges:
        branch_node = edge["node"]["name"]
        branches.append(branch_node)
    # See if there are more pages to retrieve
    query_has_next_page = results["pageInfo"]["hasNextPage"]
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
query {
  repository(owner: "$owner", name: "$name") {
    refs(query: "$branch", refPrefix: "refs/heads/", first: 1) {
      edges {
        node {
          target {
            ... on Commit {
              history(first: 100, after: $after) {
                edges {
                  node {
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
                      edges {
                        node {
                          oid
                        }
                      }
                      pageInfo {
                        hasNextPage
                        endCursor
                      }
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
        query_commits = gql(
            query_commits_template.substitute(owner=GITHUB_REPO_OWNER,
                                            name=GITHUB_REPO_NAME,
                                            branch=branch,
                                            after=end_cursor)
        )
        results = client.execute(query_commits)["repository"]["refs"]["edges"][0]["node"]["target"]["history"]
        # Add newly-encountered commits to list
        for c in results["edges"]:
            # Only add a commit to list if its not already known
            if c["node"]["oid"] not in commit_oids:
                commit_oids.append(c["node"]["oid"])
                # Append relevant commit metadata to known commits list
                commit = {"oid": c["node"]["oid"],
                        "commit_url": c["node"]["commitUrl"],
                        "commit_message_headline": c["node"]["messageHeadline"],
                        "committer_name": c["node"]["committer"]["name"],
                        "committer_email": c["node"]["committer"]["email"],
                        "commit_date": c["node"]["committedDate"],
                        "parent_oids": []}
                # Append parent commit(s) oid(s) to a list in commit object
                for parent in c["node"]["parents"]["edges"]:
                    commit["parent_oids"].append(parent["node"]["oid"])
                commits.append(commit)
        # See if there are more pages to retrieve, if so will loop again
        query_has_next_page = results["pageInfo"]["hasNextPage"]
        if query_has_next_page:
            # Get end cursor of current page so next loop will know where to start
            end_cursor = results["pageInfo"]["endCursor"]
            end_cursor = f'"{end_cursor}"' # Add extra quotes
            query_page = query_page + 1
    # Reset loop counters for next branch/iteration
    query_has_next_page = True
    query_page = 1
    end_cursor = "null"

# Print total number of commits
print(f"Total commits in repository {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}: {len(commit_oids)}",
      file=stderr)

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

exit(0)