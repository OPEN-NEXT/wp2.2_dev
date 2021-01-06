#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This is the dashboard's main module.
It defines a main function to be executed, representing execution of the
whole package. This function is high-level and calls other internal modules
that contain the actual plumbing.
"""

# Python Standard Library import(s)
import sys

# External import(s)
import pandas

# Internal import(s)
if __name__ == "__main__": 
    from preprocess import read_config, stage_data
    from miner import mine
else:
    from . preprocess import read_config, stage_data
    from . miner import mine

# High-level `main()` that spells out high-level data-mining logic

def main():
    """
    docstring
    """
    print(f"Start of main() in __main__.py")

    #
    # Read configuration file
    #

    configuration: dict = read_config()

    #
    # Read repositories list and stage existing data
    #

    staged_data: pandas.core.frame.DataFrame = stage_data(configuration["repo_list"])

    #
    # Retrieve version control data from repositories
    #

    mined_data: dict = mine(staged_data, GitHub_token=configuration["GitHub_token"])

    print(f"foobar")

if __name__ == "__main__":
    main()
    sys.exit(0)