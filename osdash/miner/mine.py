#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""[summary]

Returns:
    [type]: [description]
"""

# Python Standard Library imports
import json
import os
import sys

# Internal imports
if __name__ == "__main__":
    # from adapters import GitHub, Wikifactory
    from GitHub import GitHub
    from Wikifactory import Wikifactory
else:
    from . GitHub import GitHub
    from . Wikifactory import Wikifactory

# External imports
import pandas

# Path to example JSON file with staged data for debugging
STAGED_DATA: str = "./staged_data-example.json"

def mine(staged_data: list, GitHub_token: str) -> list:
    """[summary]

    Args:
        staged_data ([type]): [description]

    Returns:
        [type]: [description]
    """

    #
    # Split staged data based on adapter type
    #

    # For now, this means GitHub and Wikifactory

    # Get GitHub repositories
    staged_GitHub_data: list = []
    for repo in staged_data: 
        if repo["Repository"]["platform"] == "GitHub":
            staged_GitHub_data.append(repo)
    # Mine those GitHub repositories
    mined_GitHub_data: list = GitHub(staged_GitHub_data, GitHub_token)


    # Get Wikifactory repos
    staged_Wikifactory_data: list = []
    for repo in staged_data: 
        if repo["Repository"]["platform"] == "Wikifactory":
            staged_Wikifactory_data.append(repo)
    mined_Wikifactory_data: list = Wikifactory(staged_Wikifactory_data)

    #
    # Combine mined data
    #

    # Initialise an empty DataFrame to hold mined results
    #mined_data: pandas.core.frame.DataFrame = pandas.DataFrame(columns=["project", "repo_platform", "repo_url", "last_mined"])
    # Initialise an empty list to hold mined results
    mined_data: list = []
    # Then add each mined result via `pandas.concat()`
    # mined_data = pandas.concat([mined_data, 
    #                             mined_GitHub_data, 
    #                             mined_Wikifactory_data], 
    #                            ignore_index=True, copy=False)
    mined_data.extend(mined_GitHub_data)
    mined_data.extend(mined_Wikifactory_data)

    return mined_data

# main() is for when running this script on its own, probably for debugging

def main():
    pass

if __name__ == "__main__": 
    main()
    sys.exit(0)