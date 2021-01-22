#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import pathlib
import sys

# External imports
import numpy
import pandas

# Internal imports
if __name__ == "__main__": 
    from read_mining_list import read_repo_list
    from past_data import read_mined_data
else: 
    from . read_mining_list import read_repo_list
    from . past_data import read_mined_data

def stage_data(repo_csv: str, mined_data: str) -> pandas.core.frame.DataFrame:
    """[summary]

    Args:
        repo_csv (str): [description]
        mined_data (str): path to compressed ZIP archive containing previously-mined data in JSON

    Returns:
        pandas.core.frame.DataFrame: [description]
    """
    print(f"Reading list of repositories and staging existing data...")

    #
    # Read list of repositories to mine
    # 

    repo_list: pandas.core.frame.DataFrame = read_repo_list(path=repo_csv)

    #
    # Read existing data
    #

    if pathlib.Path(mined_data).exists() and pathlib.Path(mined_data).is_file(): 
        print(f"Reading past data from: {mined_data}", file=sys.stderr)
        past_data: list = read_mined_data(path=mined_data)
    else: 
        print(f"{mined_data} doesn't seem to exist.", file=sys.stderr)
        past_data: list = []

    

    #
    # Find last timestamp at which each repository was mined
    #

    # TODO: Find last mined timestamps.

    #
    # Append last-mined timestamps to list of repositories
    #

    # For now, just append an empty column to `repo_list`. Once there is prior
    # data, probably need to do some sort of Pandas join operation based on 
    # `repo_url`?
    repo_list["last_mined"] = numpy.nan

    return repo_list

def main():
    print(f"Running stage_data.py's main()...")
    repos = stage_data("input/OSH-repos-GitHub-test.csv")
    sys.exit(0)

if __name__ == "__main__":
    main()