#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports

# External imports
import pandas

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