# The api exposed by wikifactory.com/api/graphql is a graphql api. This example uses
# a python graphql client implementation to demonstrate a few possible use cases:
# https://github.com/graphql-python/gql
#
# Please install graphql-python/gql with:
# pip install --pre gql
#
# It also possible to introspect the api and see all exposed graphql queries and
# mutations in the graphiql interface running at:
# https://wikifactory.com/api/graphql

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from string import Template
import sys


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
        if len(ret) > 100:
            break

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
# information about a project. This functions is used to demonstrate how to
# get the contributions of a projects, and all of the files in the projects
# repository.
def query_project_contributions(id):
    # The query getting a project by its id, then following the contributions
    # edge to all of its contributions, and the contribution(no 's'! singular)
    # edge to its "head" contribution and getting all files from that "head"
    # contribution.
    t = Template(
        """
        query {
          project(id: "$id") {
            result {
              name
              contributions {
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
              contribution {
                files {
                  filename
                  dirname
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
    return project


if __name__ == "__main__":
    sample_transport = RequestsHTTPTransport(
        url="https://dev.wikifactory.com/api/graphql", verify=True, retries=3
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

    most_followed_otto_project = otto_projects[0]
    print(
        "Showing contributions of the most followed otto project: {name}".format(
            name=most_followed_otto_project.get("name", None)
        )
    )

    repo = query_project_contributions(most_followed_otto_project.get("id", None))
    print(repo)
