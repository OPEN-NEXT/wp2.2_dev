#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This is the dashboard's main data-mining module.
It defines a main function to be executed, representing execution of the
whole package. This function is high-level and calls other internal modules
that contain the actual plumbing.
"""

# Python Standard Library imports
import pathlib
import sys

# External imports

# Internal imports
if __name__ == "__main__": 
    # from preprocess import read_config, stage_data
    from preprocess import stage_data
else:
    # from . preprocess import read_config, stage_data
    from . preprocess import stage_data

# Some constants

# Default location to store mined data JSON file
DATA_DIR: str = "./data"
DATA_FILE: str = "mined_data.zip"
# Form mined data file path
data_path: pathlib.Path = pathlib.Path(DATA_DIR) / pathlib.Path(DATA_FILE)

# High-level `main()` that spells out high-level dashboard logic
def main():
    """
    docstring
    """
    
    #
    # Stage data mined from repositories
    #

    staged_data: list = stage_data(str(data_path))

    #
    # Derive metrics
    # 

    # TODO: Derive metrics

    #
    # Create Dash app
    #

    # TODO: Create Dash app

    #
    # Run Dash app server
    #

    # TODO Run app

    print(f"Reached end of dashboard `main()`", file=sys.stderr)

if __name__ == "__main__":
    main()
    sys.exit(0)