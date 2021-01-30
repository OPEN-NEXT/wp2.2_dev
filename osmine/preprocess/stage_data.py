#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import pathlib
import sys

# External imports
import pandas

# Internal imports
if __name__ == "__main__": 
    from read_mining_list import read_repo_list
    from past_data import read_mined_data
else: 
    from . read_mining_list import read_repo_list
    from . past_data import read_mined_data

def stage_data(repo_csv: str, mined_data: str) -> list:
    """[summary]

    Args:
        repo_csv (str): [description]
        mined_data (str): path to compressed ZIP archive containing previously-mined data in JSON

    Returns:
        list: [description]
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
        staged_data: list = read_mined_data(path=mined_data)
    else: 
        print(f"{mined_data} doesn't seem to exist.", file=sys.stderr)
        staged_data: list = []

    #
    # Record new repositories not mined before
    #

    # Get list of previously-mined repositories first
    past_repo_list: list = []
    for repo in staged_data: 
        past_repo_list.append(repo["Repository"]["repo_url"])

    # If there is a new un-mined repository, add new entry to staged data
    for url in list(repo_list["repo_url"]):
        if url in past_repo_list:
            pass
        else:
            # Create new entry for this new repository
            new_repo: dict = {
                "Repository": {
                    "project": repo_list[repo_list["repo_url"] == url]["project"].values[0],
                    "platform": repo_list[repo_list["repo_url"] == url]["repo_platform"].values[0],
                    "repo_url": url, 
                    "last_mined": "" # Empty string since it has not been mined before
                },
                "Branches": [],
                "Commits": [],
                "Tickets": []
            }
            staged_data.append(new_repo) 

    # Now, we have a set of staged data that contains previously-mined repositories
    # and possibly new ones. Each one would either have a string of the last-mined
    # timestamp or an empty string if it's a new repository.
    return staged_data

def main():
    print(f"Running stage_data.py's main()...")
    repos = stage_data("input/OSH-repos-GitHub-test.csv", "data/mined_data.zip")

if __name__ == "__main__":
    main()
    sys.exit(0)