#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""[summary]
Wikifactory API adapter/interface for data mining script
"""

# Python Standard Library imports
import datetime
import math
import string
import sys
import time
import urllib.parse

# External imports
import pandas
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
# An arbitrarily early "last minted" timestamp if a repository has not been 
# mined before
DEFAULT_LAST_MINED: str = "1970-01-01T00:00:00.000000+00:00"

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

# Get a Wikifactory project's metadata, contributions, and issues
def get_project_data(repo: dict):
    """[summary]
    Using the Wikifactory GraphQL API
    Args:
        repo (str): [description]
    """
    # Fetch data

    # Track if there is a next page of results
    query_has_next_page: bool = True
    # Track results page number
    query_page: int = 1
    # Create a pagination cursor
    end_cursor: str = "null" # "null" because there is no cursor for first query
    # Initialise an empty list of contributions
    contributions: list = []
    # Initialise an empty list of issues
    issues: list = []

    # The main structure of the query, with space for `tracker` and 
    # `contributions` elements
    main_query: string.Template = string.Template(
    """
    {
        project(space: $space, slug: $slug) {
            result {
                id
                title
                creator {
                    id
                    username
                }
                dateCreated
                lastActivityAt
                license {
                    name
                    title
                }
    $contributions_fragment
    $tracker_fragment
            }
        }
    }
    """
    )
    # Query fragement for `contributions`
    contributions_fragement: string.Template = string.Template(
    """
                contributions(after: $contributions_after, sortBy: "dateCreated") {
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
    tracker_fragment: string.Template = string.Template(
    """
                tracker {
                    issues(after: $issues_after, sortBy: "dateCreated") {
                        edges {
                            node {
                                id
                                issueSlug
                                type
                                dateCreated
                                lastUpdated
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

    print(f"Retrieving {repo['space']}/{repo['slug']}'s issues metadata...", file=sys.stderr)
    


def Wikifactory(repo_list: pandas.core.frame.DataFrame) -> dict:
    """
    docstring
    """
    print(f"Begin Wikifactory adapter")
    
    # Create column indicating if there was error when making query
    repo_list["error"] = bool(False)

    # Convert data into a list of dictionaries via the `to_dict()` "records"
    # argument.
    repo_list = repo_list.to_dict("records")

    # Go through each repository URL and fetch data
    for repo in repo_list: 
        # Track if there has been an API query error for this repository
        repo_error: bool = False

        print(f"Processing: " + repo["repo_url"])

        repo_url: str = repo["repo_url"]

        # Get "space" and "slug" components from this repository's URL
        repo_url_components: dict = parse_url(url=repo_url)

        last_mined: str = repo["last_mined"]
        # Get current timestamp to record as last mined time in exported data
        # The `datetime.timezone.utc` argument tells now() to use UTC timezone
        # (or use datetime.datetime.utcnow())
        timestamp_object: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        date_now: str = str(timestamp_object.date())
        time_now: str = str(timestamp_object.time())
        timestamp_now: str = str(date_now + "T" + time_now + "Z")

        # If there is no `last_mined` timestamp, then this `repo_url` has not 
        # been mined before. If so, set `last_mined` to some arbitrarily early
        # time: 
        if math.isnan(last_mined): # If there's not last mined time it will be `nan`
            last_mined: str = "1970-01-01T00:00:00.000000+00:00"
        else:
            pass

        # Query for the data now
        if repo_error == False: 
            try:
                response_data = get_project_data(repo=repo_url_components)
                repo["issues"] = None
                repo["commits"] = None
            except WikifactoryAPIError:
                print(f"There has been an error querying issues in this repository.")
                repo_error = True
                repo["error"] = True
        else: 
            pass

        # Combine and format results
        if repo_error == False: 
            repo["last_mined"] = timestamp_now
    
    return repo_list