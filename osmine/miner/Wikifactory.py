#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""[summary]
Wikifactory API adapter/interface for data mining script
"""

# Python Standard Library imports
import datetime
import string
import sys
import time
import urllib.parse

# External imports
import requests

#
# Define basic parameters for Wikifactory API
#

# Wikifactory GraphQL API endpoint
GRAPHQL_URL: str = "https://wikifactory.com/api/graphql"
# Wikifactory API query success response code
SUCCESS_CODE: int = 200
# Wikifactory API query response codes when retry will be attempted
RETRY_CODES: list = [429, 500, 502, 503, 504]
# Initial retry wait time in seconds
RETRY_WAIT: int = 10
# Numbers of times to retry before fail
RETRIES: int = 5
# Requested results per page for each API response
PER_PAGE: int = 100
# An arbitrarily early "last mined" timestamp if a repository has not been 
# mined before
DEFAULT_LAST_MINED: str = "1970-01-01T00:00:00.000000+00:00"
# License mappings from Wikifactory API [1] to standard SPDX license strings [2]
# [1]: Via `abreviation` field from Wikifactory API's `licenses` base query
# [2]: https://spdx.org/licenses/
# Note: Some Wikifactory licenses like "permissive" doesn't have an SPDX 
# equivalent and will not be mapped here.
LICENSE_MAP: dict = {
    "CC-BY-4.0": "CC-BY-4.0",
    "CC0-1.0": "CC0-1.0",
    "MIT": "MIT",
    "BSD-2-Clause": "BSD-2-Clause",
    "CC-BY-SA-4.0": "CC-BY-SA-4.0",
    "GPL-3.0": "GPL-3.0-only",
    "OHL": "TAPR-OHL-1.0",
    "CERN OHL": "CERN-OHL-1.2"
}

# Define a custom exception for when queries fail repeatedly
class WikifactoryAPIError(Exception): 
    pass

# Function for making queries
def make_query(query: str): 
    # Basic potato check if query looks like GraphQL
    if ("{" in query) and ("}" in query):
        print(f"Looks like a GraphQL query...")
        query_success: bool = False
        retries: int = 0
        while not query_success: 
            try:
                query_response: requests.models.Response = requests.post(url=GRAPHQL_URL, 
                                                                         json={"query": query})
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
                        raise WikifactoryAPIError(f"Retried {retries} times. Problem with query with return code {query_response.status_code}.")
                else:
                    raise WikifactoryAPIError(f"Problem with query with return code {query_response.status_code}.")
            except ConnectionError:
                if retries < RETRIES: 
                    print(f"ConnectionError - Retrying in {RETRY_WAIT} seconds.", file=sys.stderr)
                    time.sleep(RETRY_WAIT)
                    retries += 1
                else:
                    raise WikifactoryAPIError(f"Retried {retries} times with ConnectionError on last try.")
    else:
        print(f"ERROR: Query does not look like GraphQL...", file=sys.stderr)
        sys.exit(1)

# Parse Wikifactory project URL to get its "space" and "slug" components
def parse_url(url: str) -> dict:
    """
    For example, given `url="https://projects.opennext.eu/@xyz-cargo-add-ons/xyz-cargo-add-ons"`, 
    (note it might not be a `wikifactory.com` domain) it would be parsed by `urllib.parse.urlparse()` 
    into components, of which the path component can be split into the "space" and "slug", i.e. 
    "@xyz-cargo-add-ons" and "xyz-cargo-add-ons".
    """
    parsed_url: urllib.parse.ParseResult = urllib.parse.urlparse(url)
    repo: dict = {
        # Get the path component of a `urlparse()`ed URL which looks like
        # "/@xyz-cargo-add-ons/xyz-cargo-add-ons", then split it by "/" where 
        # first part would be "space", second part would be "slug". 
        # E.g. https://projects.opennext.eu/@xyz-cargo-add-ons/xyz-cargo-add-ons 
        # would have space "@xyz-cargo-add-ons" and slug "@xyz-cargo-add-ons".
        "space": getattr(parsed_url, "path").split(sep="/")[1],
        "slug": getattr(parsed_url, "path").split(sep="/")[2]
    }
    return repo

# Process contribution object from Wikifactory API into ForgeFed model
def process_contributions(contribs: list, known_contribs: list, repo_url: str) -> list:
    """[summary]

    Args:
        contrib_edge (dict): Project.contributions.edges
        known_contribs (list)
        repo_url (str)

    Returns:
        list: [description]
    """
    contributions_list: list = []

    for edge in contribs:
        if edge["node"]["id"] in known_contribs:
            pass
        else:
            if edge["node"]["parent"] is None:
                c_parents: str = ""
            else:
                c_parents: str = edge["node"]["parent"]["id"]
            c: dict = {
                "committedBy": edge["node"]["creator"]["username"],
                "committed": edge["node"]["dateCreated"],
                "hash": edge["node"]["id"],
                "summary": edge["node"]["title"],
                "parents": c_parents,
                "url": get_contrib_url(repo_url=repo_url, contrib_slug=edge["node"]["slug"])
            }
            contributions_list.append(c)

    return contributions_list

# Process issue object from Wikifactory API into ForgeFed model
def process_issues(issues: dict, known_issues: list, repo_url: str) -> list: 
    """[summary]

    Args:
        issues (dict): Project.tracker.issues.edges
        known_issues (list): [description]
        repo_url (str): [description]

    Returns:
        list: [description]
    """
    issues_list: list = []

    for edge in issues:
        if edge["node"]["id"] in known_issues:
            pass
        else:
            # Get resolved status
            if edge["node"]["status"] == "Open":
                i_resolved: bool = False
                i_resolved_time: str = ""
            else:
                i_resolved: bool = True
                i_resolved_time: str = edge["node"]["lastActivityAt"]
            # Get participants
            i_participants: list = [edge["node"]["creator"]["username"]]
            for assignee in edge["node"]["assignees"]:
                if not (assignee["username"] in i_participants):
                    i_participants.append(assignee["username"])
            for commenter in edge["node"]["commenters"]:
                if not (commenter["username"] in i_participants):
                    i_participants.append(commenter["username"])
            i: dict = {
                "attributedTo": edge["node"]["creator"]["username"],
                "summary": edge["node"]["title"],
                "published": edge["node"]["dateCreated"],
                "isResolved": i_resolved,
                "resolved": i_resolved_time,
                "id": edge["node"]["id"],
                "participants": i_participants,
                "url": get_issue_url(repo_url=repo_url, issue_slug=edge["node"]["slug"])
            }
            issues_list.append(i)
    
    return issues_list

# Process project URL and contribution slug to create contribution URL
def get_contrib_url(repo_url: str, contrib_slug: str) -> str: 
    """[summary]

    Args:
        repo_url (str): e.g. https://wikifactory.com/+OttoDIY/otto-turtle-drawing-robot
        contribution (str): e.g. 245367-416eeef63f6500bb79f10d23a623dd0c58c956ea

    Returns:
        str: [description]
    """
    return repo_url + "/contributions/" + contrib_slug.split("-")[1][0:7]

# Process project URL and issue slug to create issue URL
def get_issue_url(repo_url: str, issue_slug: str) -> str: 
    """[summary]

    Args:
        repo_url (str): e.g. https://wikifactory.com/+OttoDIY/otto-turtle-drawing-robot
        issue (str): e.g. congratulations-your-entry-has-been-approved-for-the-challenge

    Returns:
        str: [description]
    """
    return repo_url + "/issues/" + issue_slug

# Get a Wikifactory project's metadata, contributions, and issues
def get_project_data(repo_url: str) -> dict:
    """[summary]
    Using the Wikifactory GraphQL API
    Args:
        repo (str): [description]
    """
    # Fetch data

    # Initialise an empty list of contributions
    contributions: list = []
    # Initialise an empty list of issues
    issues: list = []
    # Get "space" and "slug" components from this repository's URL
    repo_url_components: dict = parse_url(url=repo_url)

    # The main structure of the query, with space for `tracker` and 
    # `contributions` elements
    main_query: string.Template = string.Template("""
    {
        project(space: "$space", slug: "$slug") {
            result {
    $project_metadata
    $contributions
    $tracker
            }
        }
    }
    """
    )
    # Query fragment for project metadata
    project_metadata_fragment: str = """
                id
                title
                creator {
                    id
                    username
                }
                dateCreated
                lastActivityAt
                forkCount
                license {
                    name
                    title
                    abreviation
                }
    """
    
    # Query fragement for `contributions`
    contributions_fragement: string.Template = string.Template("""
                contributions(first: 25, after: "$contributions_after", sortBy: "dateCreated") {
                    edges {
                        node {
                            id
                            slug
                            title
                            dateCreated
                            creator {
                                username
                            }
                            commenters {
                                username
                            }
                                parent {
                                id
                            }
                            parentSlug
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
    """
    )
    # Query fragment for `tracker`
    tracker_fragment: string.Template = string.Template("""
                tracker {
                    issues(first: 20, after: "$issues_after", sortBy: "dateCreated") {
                        edges {
                            node {
                                id
                                slug
                                type
                                dateCreated
                                lastUpdated
                                lastActivityAt
                                title
                                status
                                creator {
                                    username
                                }
                                commenters {
                                    username
                                }
                                assignees {
                                    username
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                }
    """
    )

    print(f"Retrieving {repo_url_components['space']}/{repo_url_components['slug']}'s data...", file=sys.stderr)

    # Start with one query for project metadata, contributions, and issues. 
    # After that, loop through each to see if it `hasNextPage` then run 
    # specific queries as needed.

    # Initialise an empty dictionary to hold mined data
    mined_data: dict = {}

    # Create starting query
    contributions_query: str = contributions_fragement.substitute(contributions_after="")
    tracker_query: str = tracker_fragment.substitute(issues_after="")
    query: str = main_query.substitute(space=repo_url_components["space"],
                                       slug=repo_url_components["slug"],
                                       project_metadata=project_metadata_fragment,
                                       contributions=contributions_query,
                                       tracker=tracker_query)

    # Make starting query
    response = make_query(query=query).json()["data"]["project"]["result"]

    # 
    # Get project metadata
    #

    # Map Wikifactory provided license names to SPDX
    if response["license"]["abreviation"] in LICENSE_MAP.keys():
        repo_license: str = LICENSE_MAP[response["license"]["abreviation"]]
    else:
        repo_license: str = response["license"]["name"]
    # Record project metadata into a dictionary
    mined_data["Repository"] = {
        "name": response["title"],
        "attributedTo": response["creator"]["username"],
        "published": response["dateCreated"],
        "project": repo_url_components["space"],
        "forkcount": response["forkCount"],
        "forks": [],
        "license": repo_license,
        "platform": "Wikifactory",
        "repo_url": repo_url,
        "last_mined": ""
    }

    # 
    # Get branches
    #

    # Wikifactory currently does not implement branches so save an empty list
    # for now
    mined_data["Branches"] = []

    #
    # Get commits and issues
    #

    # Process contributions from starting query

    # Create a list to hold contribution `id`s
    contribution_ids: list = []

    contributions.extend(process_contributions(contribs=response["contributions"]["edges"], 
                                               known_contribs=contribution_ids, 
                                               repo_url=repo_url))
    for c in contributions:
        contribution_ids.append(c["hash"])
    
    # Process issues from starting query

    # Create a list to hold issue `id`s
    issue_ids: list = []

    issues.extend(process_issues(issues=response["tracker"]["issues"]["edges"], 
                                 known_issues=issue_ids, 
                                 repo_url=repo_url))
    for i in issues:
        issue_ids.append(i["id"])
    
    # Make more queries as long as there is `hasNextPage == True`
    contributions_next_page: bool = response["contributions"]["pageInfo"]["hasNextPage"]
    issues_next_page: bool = response["tracker"]["issues"]["pageInfo"]["hasNextPage"]
    if contributions_next_page or issues_next_page:
        # Track if there is a next page of results
        query_has_next_page: bool = True
        contributions_end_cursor: str = response["contributions"]["pageInfo"]["endCursor"]
        issues_end_cursor: str = response["tracker"]["issues"]["pageInfo"]["endCursor"]
        while query_has_next_page:
            if contributions_next_page and issues_next_page:
                print(f"There are more contributions and issues to query...", file=sys.stderr)
                # Query for more contributions and issues
                contributions_query = contributions_fragement.substitute(contributions_after=contributions_end_cursor)
                tracker_query = tracker_fragment.substitute(issues_after=issues_end_cursor)
                query = main_query.substitute(space=repo_url_components["space"],
                                              slug=repo_url_components["slug"],
                                              project_metadata="",
                                              contributions=contributions_query,
                                              tracker=tracker_query)
                response = make_query(query=query).json()["data"]["project"]["result"]
                # Save new results
                contributions.extend(process_contributions(contribs=response["contributions"]["edges"], 
                                                           known_contribs=contribution_ids, 
                                                           repo_url=repo_url))
                for c in contributions:
                    contribution_ids.append(c["hash"])
                issues.extend(process_issues(issues=response["tracker"]["issues"]["edges"], 
                                             known_issues=issue_ids, 
                                             repo_url=repo_url))
                for i in issues:
                    issue_ids.append(i["id"])
                # Update cursors and check if there's next page of results
                contributions_end_cursor = response["contributions"]["pageInfo"]["endCursor"]
                issues_end_cursor = response["tracker"]["issues"]["pageInfo"]["endCursor"]
                contributions_next_page = response["contributions"]["pageInfo"]["hasNextPage"]
                issues_next_page = response["tracker"]["issues"]["pageInfo"]["hasNextPage"]
            elif contributions_next_page:
                print(f"There are more contributions to query...", file=sys.stderr)
                # Query for more contributions
                contributions_query = contributions_fragement.substitute(contributions_after=contributions_end_cursor)
                query = main_query.substitute(space=repo_url_components["space"],
                                              slug=repo_url_components["slug"],
                                              project_metadata="",
                                              contributions=contributions_query,
                                              tracker="")
                response = {}
                response = make_query(query=query).json()["data"]["project"]["result"]
                # Save new results
                contributions.extend(process_contributions(contribs=response["contributions"]["edges"], 
                                                           known_contribs=contribution_ids, 
                                                           repo_url=repo_url))
                for c in contributions:
                    contribution_ids.append(c["hash"])
                # Update cursors and check if there's next page of results
                contributions_end_cursor = response["contributions"]["pageInfo"]["endCursor"]
                contributions_next_page = response["contributions"]["pageInfo"]["hasNextPage"]
            elif issues_next_page:
                print(f"There are more issues to query...", file=sys.stderr)
                # Query for more issues
                tracker_query = tracker_fragment.substitute(issues_after=issues_end_cursor)
                query = main_query.substitute(space=repo_url_components["space"],
                                              slug=repo_url_components["slug"],
                                              project_metadata="",
                                              contributions="",
                                              tracker=tracker_query)
                response = make_query(query=query).json()["data"]["project"]["result"]
                # Save new results
                issues.extend(process_issues(issues=response["tracker"]["issues"]["edges"], 
                                             known_issues=issue_ids, 
                                             repo_url=repo_url))
                for i in issues:
                    issue_ids.append(i["id"])
                # Update cursors and check if there's next page of results
                issues_end_cursor = response["tracker"]["issues"]["pageInfo"]["endCursor"]
                issues_next_page = response["tracker"]["issues"]["pageInfo"]["hasNextPage"]
            else:
                print(f"Done with queries", file=sys.stderr)
                query_has_next_page = False
    
    print(f"There are {len(contribution_ids)} contributions and {len(issue_ids)} issues in this project", file=sys.stderr)
    
    # Combine data
    mined_data["Commits"] = contributions
    mined_data["Tickets"] = issues
    return mined_data

def Wikifactory(repos: list) -> list:
    """
    docstring
    """
    print(f"Begin Wikifactory adapter", file=sys.stderr)
    
    # track if there was error when making query
    mining_error: bool = False

    # Convert data into a list of dictionaries via the `to_dict()` "records"
    # argument.
    # repo_list = repo_list.to_dict("records")

    # Create a list to hold data mined from each repository
    mined_repos: list = []

    # Go through each repository URL and fetch data
    for repo in repos: 

        print(f"Processing: " + repo["Repository"]["repo_url"], file=sys.stderr)

        repo_url: str = repo["Repository"]["repo_url"]

        # Get current timestamp to record as last mined time in exported data
        # The `datetime.timezone.utc` argument tells `now()` to use UTC timezone
        # (or use `datetime.datetime.utcnow()`)
        timestamp_object: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        date_now: str = str(timestamp_object.date())
        time_now: str = str(timestamp_object.time())
        timestamp_now: str = str(date_now + "T" + time_now + "Z")

        # If there is no `last_mined` timestamp, then this `repo_url` has not 
        # been mined before. If so, set `last_mined` to some arbitrarily early
        # time: 
        # (this is currently unused because the Wikifactory API doesn't filter
        # results by timestamp)
        if repo["Repository"]["last_mined"] == "": 
            last_mined: str = DEFAULT_LAST_MINED
        else:
            last_mined: str = repo["Repository"]["last_mined"]

        # Query for the data
        if mining_error == False: 
            try:
                response_data: dict = get_project_data(repo_url=repo_url)
                response_data["Repository"]["last_mined"] = timestamp_now
                mined_repos.append(response_data)
            except WikifactoryAPIError:
                print(f"There has been an error querying this repository.", file=sys.stderr)
                mining_error = True
        else: 
            pass
    
    return mined_repos