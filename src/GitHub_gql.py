#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# This script is an initial exploration of using GitHub's version 4 GraphQL
# API to fetch the commit history of a given repository and construct a 
# viewable GraphML visualisation.
#
# The goal is to eventually incorporate this into the next generation data
# mining script for open source hardware repositories hosted on GitHub.

# TODO: Allow specifying time window for queries.
# TODO: Check rate limit before running and raise Warnings and Errors as needed
# TODO: Implement identity management
# TODO: Consider replacing gql library with built-in requests library?????

import sys
from string import Template
from sys import stderr

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

#
# Set basic parameters for this script
#

# GitHub API GraphQL API endpoint
GITHUB_API_URL: str = "https://api.github.com/graphql"
# Path to GitHub API authorisation token file
TOKEN_PATH: str = "token"
# GitHub repository's owner
GITHUB_REPO_OWNER: str = "OPEN-NEXT"
# GitHub repository's name
GITHUB_REPO_NAME: str = "wp2.2_dev"

#
# Process GitHub API token
#

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

#
# Query for repository's branches
#

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
    refs(first: 4, refPrefix: "refs/heads/", after: $after) {
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
n_branches: int = len(branches)
print(f"Got all {n_branches} branches", file=stderr)

#
# Query for commits using branches information
#

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



exit(0)

query = gql(
"""
query {
  repository(owner: "github", name: "linguist") {
    refs(first: 20, refPrefix: "refs/heads/", after: $after) {
      totalCount
      edges {
        node {
          name
          target {
            ... on Commit {
              history(first: 5) {
                edges {
                  node {
                    oid
                    author {
                      name
                    }
                  }
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

print("Printing result from query:")
print(result)

pass
exit(0)

def query_all_projects(client, tag="", sortBy="", contains="[]"):
    ret = []

    print(
        "Querying projects with tag={tag}, sortBy={sortBy}, contains={contains}...".format(
            tag=tag, sortBy=sortBy, contains=contains
        )
    )

    # Querying all projects is discouraged, but possible. The api has so far been designed with
    # mostly internal use cases in mind, therefore it may feel somewhat awkward to use for data
    # analysis purposes. In this particular case the function to query all projects needs to
    # do pagination to get all projects since our api enforces a limit how many projects can
    # be queried at once.
    hasNextPage = True
    after = ""
    if tag != "":
        tag = 'tag:"{tag}",'.format(tag=tag)
    while hasNextPage is True:
        # The actual query to get all projects, some(not all) arguments to this query are:
        # sortBy: "followers", "contributions", "likes" or most "recent" (a minus '-' before
        #         the sorting reverses the order, e.g. "-followers")
        # tag: return projects matching a certain tag, only one tag can be queried currently
        # contains: returning projects containing a field matching a string,
        #           e.g. ["name", "word"] or ["slug", "otto"] would be a way to query
        #           projects which have a name or slug(the last part of a projects url which
        #           is like the name) matching a certain word
        # first, last, after, before: arguments used for pagination
        #
        # This query only queries projects ids and their tags, but could be modified
        # to query all fields exposed by a project, refer to the schema documentation
        # in https://wikifactory.com/api/graphql to see other possible field names.
        t = Template(
            """
            query {
              projects($after $tag first:25, sortBy:"$sortBy", contains:$contains) {
                result {
                  pageInfo {
                    hasNextPage
                    endCursor
                  }
                  edges {
                    node {
                      id
                      name
                      slug
                      followersCount
                      followingCount
                      likesCount
                      contributionCount
                      commentsCount
                      starCount
                      pageviewsCount
                      archiveDownloadCount
                      space {
                        content {
                          type
                          slug
                        }
                      }
                      tags {
                        name
                      }
                    }
                  }
                }
              }
            }
            """
        )
        query = gql(
            t.substitute(after=after, tag=tag, sortBy=sortBy, contains=contains)
        )

        projects_query = client.execute(query)
        result = projects_query.get("projects", {}).get("result", {})
        page = result.get("pageInfo", {})
        edges = result.get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            ret.append(node)

        hasNextPage = page.get("hasNextPage", False)
        if hasNextPage:
            after = 'after:"{after}",'.format(after=page["endCursor"])

    print("Done querying {n} projects.".format(n=len(ret)))
    return ret


# We want to demonstrate narrowing the specific projects by certain tags, as this is the
# prefered way to interact with the api. But to know which tags are available we can
# query a all projects and get the tags from all of them with this function.
def normalize_tags(projects):
    tags = {}
    for project in projects:
        for tag in project.get("tags", []):
            name = tag.get("name", None)
            if name is not None:
                tags[name] = True
    return tags.keys()


# The url on wikifactory can be constructed from a project but this needs to be done
# manually, this piece of code may actually be incomplete or incorrect, but it works
# well enough for this example.
def make_project_url(project):
    projectSlug = project.get("slug", None)

    space = project.get("space", {})
    spaceContent = space.get("content", {})
    contentType = spaceContent.get("type", "profile")
    contentSlug = spaceContent.get("slug", None)

    typeSymbol = "@"
    if contentType == "initiative":
        typeSymbol = "+"

    t = Template("https://wikifactory.com/$typeSymbol$contentSlug/$projectSlug")
    return t.substitute(
        typeSymbol=typeSymbol, contentSlug=contentSlug, projectSlug=projectSlug
    )


# Instead of querying multiple projects with "projects", it can be beneficial to
# query the api for a specific project id and use this approach to get more
# information about a project. The next two functions demonstrate how to
# get the contributions of a project, and all of the files in a projects
# repository.
def query_project_contributions(id):
    contributions = []

    # We are querying a project by its id, then follow the contributions
    # edge to enumerate all contributions (like commits in git) to that
    # project.
    hasNextPage = True
    after = ""
    while hasNextPage:
        # Notice how the contributions edge is a connection(containts a pageInfo)
        # that requires you to do pagination to get all contributions. Very similar
        # to what we had to do in the query_all_projects function, but this time
        # for a deeper nested edge.
        t = Template(
            """
            query {
              project(id: "$id") {
                result {
                  contributions($after first:25, sortBy:"recent") {
                   pageInfo {
                     hasNextPage
                     endCursor
                    }
                    edges {
                      node {
                        version
                        title
                        dateCreated
                        creator {
                          username
                        }
                      }
                    }
                  }
                }
              }
            }
            """
        )
        query = gql(t.substitute(id=id, after=after))
        project_query = client.execute(query)
        result = (
            project_query.get("project", {}).get("result", {}).get("contributions", {})
        )
        page = result.get("pageInfo", {})
        edges = result.get("edges", [])
        for edge in edges:
            node = edge.get("node", {})
            contributions.append(node)

        hasNextPage = page.get("hasNextPage", False)
        if hasNextPage:
            after = 'after:"{after}",'.format(after=page["endCursor"])

    return contributions


def query_project_files(id):
    # In addition to the contributionS edge there is also a contribution(no 's'! singular)
    # edge that points the most recent contribution. We follow that contribution edge to
    # the "head" contribution and then get all files of the projects from "head", meaning
    # we get all files representing the latest state of the projects file repository.
    t = Template(
        """
        query {
          project(id: "$id") {
            result {
              contribution {
                files {
                  filename
                  dirname
                  isFolder
                }
              }
            }
          }
        }
        """
    )
    query = gql(t.substitute(id=id))
    project_query = client.execute(query)
    project = project_query.get("project", {}).get("result", {})
    files = project.get("contribution", {}).get("files", [])
    return files


# Main section of this example script, just calling the functions as demonstration
# and outputing their results in a somewhat nice to read format.
if __name__ == "__main__":
    sample_transport = RequestsHTTPTransport(
        url="https://wikifactory.com/api/graphql", verify=True, retries=3
    )

    client = Client(transport=sample_transport, fetch_schema_from_transport=True)

    # this can be used to get all tags:
    # all_projects = query_all_projects(client)
    # print(normalize_tags(all_projects))

    # this could be used to search all projects with a name matching "notebook"
    notebook_projects = query_all_projects(client, contains='["name","notebook"]')
    for notebook in notebook_projects:
        print(
            "Project: "
            + "followers: "
            + str(notebook.get("followersCount", 0))
            + ", name: "
            + notebook.get("name", None)
            + ", url: "
            + make_project_url(notebook)
        )
    print("")

    # this gets all projects which are tagged with "ottodiy"
    # sorted by number of contributions in descending order
    otto_projects = query_all_projects(client, tag="ottodiy", sortBy="followers")

    if len(otto_projects) == 0:
        print(
            """
                We expected you to receive ottodiy projects at this point,
                but since you didn't, something must have gone wrong.
            """
        )
        sys.exit(1)

    for otto in otto_projects:
        print(
            "Project: "
            + "followers: "
            + str(otto.get("followersCount", 0))
            + ", name: "
            + otto.get("name", None)
            + ", url: "
            + make_project_url(otto)
        )
    print("")

    # we'll show all contributions of the most followed ottodiy project
    # in a similar format to what git log would output
    most_followed_otto_project = otto_projects[0]
    print(
        "Showing contributions of the most followed otto project: {name}".format(
            name=most_followed_otto_project.get("name", None)
        )
    )

    contributions = query_project_contributions(
        most_followed_otto_project.get("id", None)
    )
    for contribution in contributions:
        t = Template(
            """\033[33mcontribution $commit\033[0m
Author: $author
Date: $date
    $title
"""
        )
        print(
            t.substitute(
                commit=contribution.get("version"),
                author=contribution.get("creator", {}).get("username"),
                date=contribution.get("dateCreated"),
                title=contribution.get("title"),
            )
        )

    # and finally we'll also list all files from the head contribution from
    # the most followed ottodiy as working urls
    print(
        "Listing all files in the repository of project: {name}".format(
            name=most_followed_otto_project.get("name", None)
        )
    )
    files = query_project_files(most_followed_otto_project.get("id", None))

    root = {}
    for f in files:
        if f.get("isFolder", False):
            continue

        dirname = f.get("dirname", "")
        if dirname != "":
            dirname += "/"
        dirfiles = root.get(dirname, [])
        dirfiles.append(f.get("filename", None))
        root[dirname] = dirfiles

    url = make_project_url(most_followed_otto_project)
    for dirname, files in root.items():
        for filename in files:
            print(
                Template("$url/file/$dirname$filename").substitute(
                    url=url, dirname=dirname, filename=filename
                )
            )
