#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# This script is an initial exploration of using GitHub's version 4 GraphQL
# API to fetch the commit history of a given repository and construct a 
# viewable GraphML visualisation.
#
# The goal is to eventually incorporate this into the next generation data
# mining script for open source hardware repositories hosted on GitHub.

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

# Read GitHub API authorisation token from file
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

client = Client(transport=transport, fetch_schema_from_transport=True)


query = gql(
"""
query {
  repository(owner: "github", name: "linguist") {
    refs(first: 20, refPrefix: "refs/heads/") {
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

result = client.execute(query)

branches: list = []

has_next_page: bool = True
after_cursor: str = ""

while has_next_page is True:
    pass

print("Printing result from query:")
print(result)

pass

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
