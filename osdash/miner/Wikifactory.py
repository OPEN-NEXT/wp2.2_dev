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



def Wikifactory(repo_list: pandas.core.frame.DataFrame) -> dict:
    """
    docstring
    """
    print(f"Begin Wikifactory adapter")
    
    # Create empty DataFrame to hold mined data
    mined_data: pandas.core.frame.DataFrame = repo_list[["repo_url", "last_mined"]]

    # For each repository (row) in `repo_list`, mine data at its URL
    # Use itertuples() because it seems to be much faster than iterrows()
    # Reference: https://stackoverflow.com/a/10739432/186904
    # TODO: Consider using Pandas's apply() instead: https://stackoverflow.com/a/30566899/186904
    for repo in repo_list.itertuples(): 
        # Since itertuples() returns data of namedtuple type, use getattr() to 
        # access items in each row
        # Reference: https://medium.com/@rinu.gour123/python-namedtuple-working-and-benefits-of-namedtuple-in-python-276d679b2e9c
        print(f"Processing: " + getattr(repo, "repo_url"))
    mined_data: pandas.core.frame.DataFrame = repo_list

    mined_data = mined_data.to_dict("records")

    return mined_data