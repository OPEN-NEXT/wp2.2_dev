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

def mine(staged_data: pandas.core.frame.DataFrame, GitHub_token: str) -> pandas.core.frame.DataFrame:
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

    # Get GitHub repos
    GitHub_repos: pandas.core.frame.DataFrame = staged_data[staged_data["repo_platform"] == "GitHub"]
    mined_GitHub_data: pandas.core.frame.DataFrame = GitHub(GitHub_repos, GitHub_token)


    # Get Wikifactory repos
    Wikifactory_repos: pandas.core.frame.DataFrame = staged_data[staged_data["repo_platform"] == "Wikifactory"]
    mined_Wikifactory_data: pandas.core.frame.DataFrame = Wikifactory(Wikifactory_repos)

    #
    # Combine mined data
    #

    # Initialise an empty DataFrame to hold mined results
    mined_data: pandas.core.frame.DataFrame = pandas.DataFrame(columns=["project", "repo_platform", "repo_url", "last_mined"])
    # Then add each mined result via `pandas.concat()`
    mined_data = pandas.concat([mined_data, 
                                mined_GitHub_data, 
                                mined_Wikifactory_data], 
                               ignore_index=True, copy=False)
    return mined_data

# main() is for when running this script on its own, probably for debugging
# Uses the example staged JSON file

def main():
    with open(STAGED_DATA) as json_file: 
        loaded_json = json.load(json_file)
        loaded_json: str = json.dumps(loaded_json)
    GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
    staged_data: pandas.core.frame.DataFrame = pandas.read_json(loaded_json, orient="columns")
    mined_data: pandas.core.frame.DataFrame = mine(staged_data, GITHUB_TOKEN)
    print(mined_data)

if __name__ == "__main__": 
    main()
    sys.exit(0)