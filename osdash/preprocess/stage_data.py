#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports

# External imports
import pandas

# Internal imports
if __name__ == "__main__": 
    from read_mining_list import read_repo_list
else: 
    from . read_mining_list import read_repo_list

def stage_data(repo_csv: str) -> pandas.core.frame.DataFrame:
    print(f"Reading list of repositories and staging existing data...")

    #
    # Read list of repositories to mine
    # 
    
    repo_list: pandas.core.frame.DataFrame = read_repo_list(path=repo_csv)

def main():
    print(f"Running state_data.py's main()...")
    read_repo_list("input/OSH-repos-GitHub-test.csv")

if __name__ == "__main__":
    main()