#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Optional, Set

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl

class Item(BaseModel): 
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class MiningRequest(BaseModel): 
    repo_urls: Set[HttpUrl] = set()
    requested_data: Set[str] = set()

# Supported hosting platforms as a list of their domains. 
# `repo_urls` need to include one of these domains.
supported_domains: list = [
    "github.com", 
    "wikifactory.com"
]

# Supported data-mining request types. Items in `required_data` must
# be from this list.
supported_data_requests: list = [
    "file_types", 
    "issue_activity_level", 
    "commits_over_time", 
    "skill_tags", 
    "manufacturing_tags", 
    "standards_tags", 
    "license", 
    "files_editable"
]

app = FastAPI()

@app.get("/")
async def root(): 
    return {"message": "Dashboard data-mining backend is on"}

@app.post("/items/")
async def create_item(item: Item): 
    item_dict: dict = item.dict()
    if item.tax: 
        price_with_tax: float = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get("/items/{item_id}")
async def read_item(item_id: int): 
    return {"requested item_id": item_id}

@app.post("/data/")
async def mining_request(request_body: MiningRequest): 
    # 
    # Check API client's request body
    #

    # Check if each repository URL is supported
    print("Handling request...")
    for url in request_body.repo_urls: 
        print(f"Checking URL: {url}")
        # See: https://stackoverflow.com/a/6531704/186904
        if any(domain in url.host for domain in supported_domains): 
            print(f"{url} domain is supported.")
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
    # Process request body
    #

    #
    # Prepare API response
    #

    response: list = []

    for repo in request_body.repo_urls: 
        repo_dict: dict = {
            "repo_url": str(repo), 
            "requested_data": dict()
        }
        for data_item in request_body.requested_data: 
            if data_item == "file_types": 
                repo_dict["requested_data"][data_item] = [
                    ".pdf", 
                    ".stl", 
                    ".md", 
                    ".dxf"
                ]
            elif data_item == "skill_tags": 
                repo_dict["requested_data"][data_item] = [
                    "3D printing", 
                    "Markdown", 
                    "PCB design"
                ]
            elif data_item == "license": 
                repo_dict["requested_data"][data_item] = {
                    "SPDX": "CERN-OHL-S-2.0", 
                    "permissions": [
                        "commercial use", 
                        "modification", 
                        "distribution", 
                        "private use"
                    ], 
                    "limitations": [
                        "liability", 
                        "warranty"
                    ], 
                    "conditions": [
                        "license and copyright notice"
                    ]
                }
            else: 
                repo_dict["requested_data"][data_item] = ""
        response.append(repo_dict)
    return response