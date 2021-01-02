#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# 
import logging
import os
import sys

def stage_data(config: dict) -> dict:
    print(f"Reading list of repositories and staging existing data...")
    staged_data: dict = dict()

    #
    # Process input list of repositories (`repo_list`) to mine
    #

    # Check if `repo_list` exists and parses correctly
    try:
        assert os.path.isfile(config["repo_list"]), "Error accessing repository list: {}".format(config["repo_list"])
    except AssertionError as no_repo_list:
        logging.critical(no_repo_list)
        sys.exit(1)
    else:
        try:
            with open(config["repo_list"], newline="") as repo_file:
                repo_csv = csv.DictReader(repo_file)
                repo_list: list = list()
                for row in repo_csv:
                    repo_list.append(row)
            del repo_file, repo_csv
        except Exception as read_csv_error: # TODO: Make Exception more specific
            logging.critical(f"Error parsing repository list: {read_csv_error}")
            sys.exit(1)
    # Check repository list format
    bad_rows: list = list() # Create an empty list to record list items in wrong format
    for row in repo_list: # TODO: More efficient way to check than go through each list item
        try: # Make sure "owner" and "repo" fields consistently exist
            assert "owner" in row and "repo" in row, "Repository list CSV file needs field names 'owner' and 'row'"
        except AssertionError as fieldname_error:
            logging.critical(fieldname_error)
            sys.exit(1)
        else:
            # Record which items don't have exactly two items, one each for "owner" and "repo", 
            # plus if there are empty (None) cells
            if len(row) != 2 or None in row.values():
                bad_rows.append(row)
    try: # If there are bad items in repository list, print them and exit
        assert len(bad_rows) == 0, "Some rows in repository list have problems: "
    except AssertionError as item_error:
        logging.critical(item_error)
        for bad_row in bad_rows:
            logging.critical(bad_row.values()) # TODO: Make this more human-readable
        sys.exit(1)
            
    # TODO: Remove duplicate entries in `repo_list`
    # Put `repo_list` into `config`
    config["repo_list"] = repo_list

    return staged_data

def main():
    print(f"Running state_data.py's main()...")

if __name__ == "__main__":
    main()