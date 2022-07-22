#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
from datetime import datetime
import json
import os
import urllib
import sys

# External imports
from fastapi import status
from fastapi.responses import JSONResponse
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Internal imports
import oshminer.filetypes as filetypes
from oshminer.errors import exceptions

# Set Wikifactory API URL
# Looks for the `WIF_API_URL` environment variable, and if not found, default to: 
# https://wikifactory.com/api/graphql
# See: 
# https://www.twilio.com/blog/environment-variables-python
WIF_API_URL_DEFAULT: str = "https://wikifactory.com/api/graphql"
WIF_API_URL: str = os.environ.get("WIF_API_URL", WIF_API_URL_DEFAULT)

async def get_files_info(project: dict, session) -> dict:
    # Provide a GraphQL query
    query = gql(
        """
        query ($space: String, $slug: String) {
            project(space: $space, slug: $slug) {
                result {
                    contributionUpstream {
                        id
                        files {
                            isFolder
                            filename
                            dirname
                            file {
                                id
                                url
                                mimeType
                            }
                        }
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "space": project["space"], 
        "slug": project["slug"]
    }
    
    # Execute the query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    API_response = await session.execute(query, variable_values = params)
    if API_response["project"]["result"] is None: 
        raise exceptions.BadRepoError # Raise error if Wikifactory API can't find this project
    # Only continue if there are files in the project
    if API_response["project"]["result"]["contributionUpstream"] is not None: 
        # Get raw file list from API response
        raw_file_list: list = API_response["project"]["result"]["contributionUpstream"]["files"]
        # Exclude folders from list
        file_list: list = [f for f in raw_file_list if f["isFolder"] is False]
        # Get file extensions
        filenames: list = [{"filename": f["filename"], "extension": f["filename"].split(".")[-1].lower()} for f in file_list]

        #
        # Get number and proportion of each file type
        #

        # TODO: Put the following actions counting the number and proportion of 
        # file types into its own module and functions, since it should be the same
        # for Wikifactory and GitHub

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
        license_files: int = len([f for f in file_list if f["filename"] == "LICENSE"])
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
    else: # If there are no files, return 0 for everything
        result: dict = {
            "files_info": {
                "total_files": 0, 
                "ecad_files": 0, 
                "mcad_files": 0, 
                "image_files": 0, 
                "data_files": 0, 
                "document_files": 0, 
                "other_files": 0, 
                "ecad_proportion": 0.0, 
                "mcad_proportion": 0.0, 
                "image_proportion": 0.0, 
                "data_proportion": 0.0, 
                "document_proportion": 0.0,
                "other_proportion": 0.0
            }
        }

    return result

async def get_issues_level(project: dict, session) -> dict: 
    # Provide a GraphQL query
    query = gql(
        """
        query ($issuesCursor: String, $space: String, $slug: String) {
            project(space: $space, slug: $slug) {
                result {
                    tracker {
                        issues(first: 100, after: $issuesCursor) {
                            edges {
                                node {
                                    id
                                    title
                                    dateCreated
                                    lastActivityAt
                                    status
                                    slug
                                }
                            }
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                            totalCount
                        }
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "space": project["space"], 
        "slug": project["slug"], 
        "issuesCursor": ""
    }
    # Create a variable to track issues pagination
    issues_has_next_page: bool = True
    # Create an empty list to populate with project issues
    issues: list = []
    # Make queries to retrieve project issues
    while issues_has_next_page: 
        # `execute_async()` is the asynchronous version of `execute()`
        API_response: dict = await session.execute(query, variable_values = params)
        if API_response["project"]["result"] is None: 
            raise exceptions.BadRepoError # Raise error if Wikifactory API can't find this project
        if API_response["project"]["result"]["tracker"]["issues"]["totalCount"] > 0: # Only continue if there are issues
            response_items: list = API_response["project"]["result"]["tracker"]["issues"]["edges"]
            for item in response_items: 
                item_slug: str = item["node"]["slug"]
                issue: dict = {
                    "id": f"https://wikifactory.com/{project['space']}/{project['slug']}/issues/{item_slug}", 
                    "published": item["node"]["dateCreated"], 
                    "isResolved": item["node"]["status"] == "Closed", 
                    "resolved": item["node"]["lastActivityAt"]
                }
                issues.append(issue)
            # Sort issues by most recent timestamp for each issue
            issues = sorted(issues, key = lambda t: datetime.strptime(t["resolved"], "%Y-%m-%dT%H:%M:%S.%f%z"))
        # Track pagination
        issues_has_next_page = API_response["project"]["result"]["tracker"]["issues"]["pageInfo"]["hasNextPage"]
        params["issuesCursor"]: str = API_response["project"]["result"]["tracker"]["issues"]["pageInfo"]["endCursor"]

    result: dict = {
        "issues_level": issues
    }
    return result

async def get_commits_level(project: dict, session) -> dict: 
    # `wp2.2_dev` issue #87 discusses relevant Wikfactory API calls: 
    # https://github.com/OPEN-NEXT/wp2.2_dev/issues/87
    # Provide a GraphQL query
    query = gql(
        """
        query ($contribCursor: String, $space: String, $slug: String) {
            project(space: $space, slug: $slug) {
                result {
                    contributions(first: 100, after: $contribCursor) {
                        edges {
                            node {
                                id
                                title
                                dateCreated
                                slug
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        totalCount
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "space": project["space"], 
        "slug": project["slug"], 
        "contribCursor": ""
    }
    # Create a variable to track contributions pagination
    contribs_has_next_page: bool = True
    # Create an empty list to populate with project contributions
    contribs: list = []
    while contribs_has_next_page: 
        # `execute_async()` is the asynchronous version of `execute()`
        API_response: dict = await session.execute(query, variable_values = params)
        if API_response["project"]["result"] is None: 
            raise exceptions.BadRepoError # Raise error if Wikifactory API can't find this project
        if API_response["project"]["result"]["contributions"]["totalCount"] > 0: # Only continue if there are contributions
            response_items: list = API_response["project"]["result"]["contributions"]["edges"]
            for item in response_items: 
                contrib: dict = {
                    "hash": item["node"]["id"], 
                    "committed": item["node"]["dateCreated"]
                }
                contribs.append(contrib)
            # Sort issues by most recent timestamp for each issue
            contribs = sorted(contribs, key = lambda t: datetime.strptime(t["committed"], "%Y-%m-%dT%H:%M:%S.%f%z"))
        # Track pagination
        contribs_has_next_page = API_response["project"]["result"]["contributions"]["pageInfo"]["hasNextPage"]
        params["contribCursor"]: str = API_response["project"]["result"]["contributions"]["pageInfo"]["endCursor"]
    
    result: dict = {
        "commits_level": contribs
    }
    return result

async def get_tags(project: dict, session) -> dict: 
    # Provide a GraphQL query
    query = gql(
        """
        query ($tagCursor: String, $space: String, $slug: String) {
            project(space: $space, slug: $slug) {
                result {
                    tags {
                        name
                    }
                    contributors(first: 100, after: $tagCursor) {
                        edges {
                            node {
                                tags {
                                    name # This shows up as "skills" on a profile page
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        totalCount
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "space": project["space"], 
        "slug": project["slug"], 
        "tagCursor": ""
    }
    # Create a variable to track user tag pagination
    user_tags_has_next_page: bool = True
    # Create an empty list to populate with project and its users' tags
    tags: list = []
    # Execute the query on the transport
    # Keep going while there is a next page of user tags
    while user_tags_has_next_page: 
        # `execute_async()` is the asynchronous version of `execute()`
        API_response: dict = await session.execute(query, variable_values = params)
        if API_response["project"]["result"] is None: 
            raise exceptions.BadRepoError # Raise error if Wikifactory API can't find this project
        # Append project level tags to list
        tags += API_response["project"]["result"]["tags"]
        # Go through a project's users and append their tags, too
        for user in API_response["project"]["result"]["contributors"]["edges"]: 
            tags += user["node"]["tags"]
        # At last page of list of users, leave this loop
        params["tagCursor"] = API_response["project"]["result"]["contributors"]["pageInfo"]["endCursor"]
        user_tags_has_next_page = API_response["project"]["result"]["contributors"]["pageInfo"]["hasNextPage"]
    # Each item in the list is currently a dictionary, extract the actual tag from it
    result: dict = {
        "tags": []
    }
    result["tags"]: list = [tag["name"] for tag in tags]
    # Deduplicate result list by using `set()` which removes duplicates
    result["tags"] = list(set(result["tags"]))
    return result

async def get_license(project: dict, session) -> dict: 
    # Provide a GraphQL query
    query = gql(
        """
        query ($space: String, $slug: String) {
            project(space: $space, slug: $slug) {
                result {
                    license {
                        name
                        title
                        link
                        abreviation
                        isHeader
                    }
                }
            }
        }
        """
    )
    # Query variables
    params: dict = {
        "space": project["space"], 
        "slug": project["slug"]
    }

    # Read list of licenses for use when incoming request asks for license information
    with open("contrib/license_list.json", encoding = "utf-8") as licenses_file: 
        license_list: list = json.load(licenses_file)
    
    # Execute the query on the transport
    # `execute_async()` is the asynchronous version of `execute()`
    API_response: dict = await session.execute(query, variable_values = params)
    if API_response["project"]["result"] is None: 
        raise exceptions.BadRepoError # Raise error if Wikifactory API can't find this project
    # Get license string for this project
    project_license: str = ""
    # Account for some response cases
    if API_response["project"]["result"]["license"] is None: 
        project_license = "unlicensed"
    elif project_license == "GPL-3.0-or-later":
        project_license = "GPL-3.0"
    else: 
        project_license: str = API_response["project"]["result"]["license"]["abreviation"]

    # Get details for that license and put it in `result`
    result: dict = {
        "license": [license for license in license_list if license["spdx_id"] == project_license][0]
    }

    return result

queries: dict = {
    "files_info": get_files_info, 
    "issues_level": get_issues_level, 
    "commits_level": get_commits_level, 
    "tags": get_tags, 
    "license": get_license
}

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

async def make_Wikifactory_request(url: str, data: list) -> dict: 
    try: 
        # First, check if there is a custom Wikifactory API URL and if it works
        if WIF_API_URL != WIF_API_URL_DEFAULT: 
            print(
                f"Checking custom Wikifactory API URL: {WIF_API_URL}", 
                file = sys.stderr
                )
            try: 
                api_url_response = urllib.request.urlopen(
                    WIF_API_URL, 
                    timeout=5
                    )
            except (urllib.error.URLError): 
                print(f"Unable to reach Wikifactory API at: {WIF_API_URL}", file=sys.stderr)
                raise exceptions.BadWIFAPIError

        print(
            f"Constructing and making an API request to Wikifactory for repository {url} for the following data {data}", 
            file = sys.stderr
        )

        # If the Wikifactory API is reacheable as tested above, then: 
        # Create a dictionary to hold results from Wikifactory API query
        results: dict = {
            "repository": str(url), 
            "platform": "Wikifactory", 
            "requested_data": {}
        }

        # Select transport with the Wikifactory API endpoint URL
        transport = AIOHTTPTransport(url = WIF_API_URL)

        # Get "space" and "slug" components from this repository's URL
        space_slug: dict = parse_url(url)

        async with Client(transport = transport, fetch_schema_from_transport = True) as session: 
            for data_type in data: 
                query_result: dict = await queries[data_type](space_slug, session)
                results["requested_data"].update(query_result)

        return results
        
    except (exceptions.BadWIFAPIError) as err: 
        return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = f"Error reaching Wikifactory API URL: {WIF_API_URL} {err}"
            )