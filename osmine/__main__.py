#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This is the dashboard's main data-mining module.
It defines a main function to be executed, representing execution of the
whole package. This function is high-level and calls other internal modules
that contain the actual plumbing.
"""

# Python Standard Library import(s)
import pathlib
import sys

# Internal import(s)
if __name__ == "__main__": 
    from preprocess import read_config, stage_data
    from miner import mine
    from postprocess import exporter
else:
    from . preprocess import read_config, stage_data
    from . miner import mine
    from . postprocess import exporter

# Some constants

# Default location to store mined data JSON file
DATA_DIR: str = "./data"
DATA_FILE: str = "mined_data.zip"
# Form mined data file path
data_path: pathlib.Path = pathlib.Path(DATA_DIR) / pathlib.Path(DATA_FILE)

# High-level `main()` that spells out high-level data-mining logic
def main():
    """[summary]
    """
    print(f"Start of main() in __main__.py")

    #
    # Read configuration file
    #

    configuration: dict = read_config()

    #
    # Read repositories list and stage existing data
    #

    staged_data: list = stage_data(configuration["repo_list"], mined_data=str(data_path))

    #
    # Retrieve version control data from repositories
    #

    mined_data: list = mine(staged_data, GitHub_token=configuration["GitHub_token"])

    #
    # Export mined data into a file
    #

    # Create directory to store data file if needed
    # TODO: Honor configuration option on whether to create a new directory, 
    # maybe fold into `save_mined_data()`.
    if pathlib.Path(DATA_DIR).exists(): 
        if pathlib.Path(DATA_DIR).is_dir(): 
            pass
        else: 
            raise Exception("Data path does not seem to be a directory.")
    else: 
        pathlib.Path(DATA_DIR).mkdir()

    exporter.save_mined_data(path=str(data_path), mined_data=mined_data)

    print(f"foobar")

if __name__ == "__main__":
    main()
    sys.exit(0)