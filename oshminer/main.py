#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import asyncio
import json
import sys

# External library imports
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl

# Internal module imports
from oshminer.supported_platforms import supported_domains
from oshminer.errors import exceptions

class MiningRequest(BaseModel): 
    repo_urls: list[HttpUrl] = set()
    requested_data: list[str] = set()

# Supported data-mining request types. Items in `required_data` must
# be from this list.
supported_data_requests: list = [
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

async def process_repo(repo: HttpUrl, requests: list[str], responses: list): 
    platform: str = repo.host.replace("www.", "")
    try: 
        repo_info: dict = await supported_domains[platform](repo, requests)
    except exceptions.BadRepoError: 
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = f"Error with repository: {repo}"
        )
    responses.append(repo_info)

@app.get(
    "/data/", 
    name = "API endpoint", 
    description = "Primary endpoint for requesting data."
    )
async def mining_request(request_body: MiningRequest): 
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

    await asyncio.gather(*[process_repo(repo, request_body.requested_data, response_list) for repo in request_body.repo_urls])

    # for repo in request_body.repo_urls: 
    #     platform = repo.host.replace("www.", "")
    #     try: 
    #         repo_info: dict = await supported_domains[platform](repo, request_body.requested_data)
    #     except exceptions.BadRepoError: 
    #         return JSONResponse(
    #             status_code = status.HTTP_400_BAD_REQUEST, 
    #             content = f"Error with repository: {repo}"
    #         )
    #     response_list.append(repo_info)

    return response_list