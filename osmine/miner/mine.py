#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""[summary]

Returns:
    [type]: [description]
"""

# Python Standard Library imports
import sys

# Internal imports
if __name__ == "__main__":
    # from adapters import GitHub, Wikifactory
    from GitHub import GitHub
    from Wikifactory import Wikifactory
else:
    from . GitHub import GitHub
    from . Wikifactory import Wikifactory

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
    staged_GitHub_data: list = []
    staged_Wikifactory_data: list = []

    for repo in staged_data:
        if repo["Repository"]["platform"] == "GitHub":
            staged_GitHub_data.append(repo)
        elif repo["Repository"]["platform"] == "Wikifactory":
            staged_Wikifactory_data.append(repo)
        else:
            print(f"{repo['Repository']['repo_url']} has unsupported platform {repo['Repository']['platform']}, skipping.", file=sys.stderr)

    # Get GitHub repositories
    mined_GitHub_data: list = GitHub(staged_GitHub_data, GitHub_token)

    # Get Wikifactory repos
    mined_Wikifactory_data: list = Wikifactory(staged_Wikifactory_data)

    #
    # Combine mined data
    #

    # Initialise an empty list ten hold mined results
    mined_data: list = []
    mined_data.extend(mined_GitHub_data)
    mined_data.extend(mined_Wikifactory_data)

    return mined_data

# main() is for when running this script on its own, probably for debugging

def main():
    pass

if __name__ == "__main__": 
    main()
    sys.exit(0)