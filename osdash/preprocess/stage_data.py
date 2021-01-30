#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import json
import pathlib
import sys
import zipfile

# Default name for mined data file in compressed archive
DATA_FILE: str = "mined_data.json"

# Function to read data from `osmine`
def read_mined_data(path: str) -> list:
    """[summary]

    Args:
        path (str): [description]

    Returns:
        list: [description]
    """
    # Read from compressed archive containing previously-mined JSON data
    with zipfile.ZipFile(path, mode="r") as zip_file: 
        # Test archive integrity first
        zip_file.testzip()
        # Extract from data file into a Python `list` object
        with zip_file.open(DATA_FILE) as JSON_file: 
            extracted_data: list = json.load(JSON_file)

    return extracted_data

# Main function to read mined data
def stage_data(mined_data: str) -> list:
    """[summary]

    Args:
        mined_data (str): path to compressed ZIP archive containing previously-mined data in JSON

    Returns:
        list: [description]
    """
    print(f"Staging existing data...", file=sys.stderr)

    #
    # Read existing data
    #

    if pathlib.Path(mined_data).exists() and pathlib.Path(mined_data).is_file(): 
        print(f"Reading past data from: {mined_data}", file=sys.stderr)
        staged_data: list = read_mined_data(path=mined_data)
    else: 
        raise Exception(f"{mined_data} doesn't seem to exist or be readable.")

    # Now, we have a set of staged data that contains previously-mined 
    # repositories.
    return staged_data

def main():
    pass

if __name__ == "__main__":
    main()
    sys.exit(0)