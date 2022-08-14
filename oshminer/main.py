#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import asyncio
import json
import http.client
import sys
import urllib

# External library imports
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl

# Internal module imports
from oshminer.supported_platforms import supported_domains
from oshminer.errors import exceptions

# Default Wikifactory API URL
WIF_API_DEFAULT: str = "https://wikifactory.com/api/graphql"
class MiningRequest(BaseModel): 
    repo_urls: list[HttpUrl] = set()
    requested_data: list[str] = set()
    wikifactory_API_URL: str = WIF_API_DEFAULT

# Supported data-mining request types. Items in `requested_data` must
# be from this list.
supported_data_requests: list = [
    "files_editability", 
    "files_info", 
    "issues_level", 
    "commits_level", 
    "tags", 
    "license"
]

app = FastAPI(
    title = "WP2.2 dashboard backend", 
    description = "A REST API to request dashboard metrics for a list of repositories on GitHub and Wikifactory."
)

@app.get(
    "/", 
    name = "Root", 
    description = "Returns a message that the API is online."
    )
async def root(): 
    return {"message": "Dashboard data-mining backend is on"}

async def process_repo(repo: HttpUrl, 
                       requests: list[str], 
                       responses: list, 
                       WIF_API: str = WIF_API_DEFAULT): 
    platform: str = repo.host.replace("www.", "")
    # If a custom Wikifactory API URL is provided, then use it.
    if WIF_API != WIF_API_DEFAULT: 
        repo_info: dict = await supported_domains[platform](repo, requests, WIF_API)
        responses.append(repo_info)
    else: 
        repo_info: dict = await supported_domains[platform](repo, requests)
        responses.append(repo_info)

@app.post(
    "/data/", 
    name = "API endpoint", 
    description = "Primary endpoint for requesting data."
    )
async def mining_request(request_body: MiningRequest): 
    #
    # Check if custom Wikifactory API URL is provided and test it
    #
    
    if request_body.wikifactory_API_URL != WIF_API_DEFAULT: 
        print(
            f"Custom Wikifactory API URL detected: {request_body.wikifactory_API_URL}", 
            file = sys.stderr
            )
        try: 
            api_url_response = urllib.request.urlopen(
                request_body.wikifactory_API_URL, 
                timeout=10
                )
            if api_url_response.status != 200: 
                raise exceptions.BadWIFAPIError
        except (exceptions.BadWIFAPIError, urllib.error.URLError, http.client.BadStatusLine) as err: 
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = f"Error reaching Wikifactory API URL: {request_body.wikifactory_API_URL} {err}"
            )
    elif request_body.wikifactory_API_URL is None: 
        request_body.wikifactory_API_URL = WIF_API_DEFAULT

    # 
    # Check API client's request body
    #

    # Check if each repository URL is supported, and if it is, add it to a list
    # of platforms for which we need to construct API queries for
    print("Handling request...", file = sys.stderr)
    platforms: list = [] # Tracks which platforms are in the received request
    for url in request_body.repo_urls: 
        print(f"Checking URL: {url}")
        # See: https://stackoverflow.com/a/6531704/186904
        if any(domain in url.host for domain in supported_domains): 
            print(f"{url} domain is supported.")
            if url.host.replace("www.", "") not in platforms: 
                platforms.append(url.host.replace("www.", ""))
            ## TODO: Also check if the repository actually exists
        else: 
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = f"Repository URL domain not supported: {url.host}"
            )
    # Check if each requested data item is supported
    for data_item in request_body.requested_data: 
        print(f"Checking requested: {data_item}")
        if any(item in data_item for item in supported_data_requests): 
            print(f"{data_item} is supported.")
        else: 
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = f"Requested data type not supported: {data_item}"
            )
    
    #
    # Prepare API response
    #

    response_list: list = []

    #
    # Construct, send API requests, and get results
    #
    
    try: 
        await asyncio.gather(
            *[
                process_repo(
                    repo, 
                    request_body.requested_data, 
                    response_list, 
                    WIF_API=request_body.wikifactory_API_URL
                    ) for repo in request_body.repo_urls
                ]
            )
    except exceptions.BadGitHubTokenError: 
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content = f"Server-side GitHub API token incorrect or not in environment variable."
        )
    except exceptions.BadRepoError: 
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = f"Error with repository: {repo}"
        )

    return response_list