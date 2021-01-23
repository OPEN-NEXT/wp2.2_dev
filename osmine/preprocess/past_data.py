#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Libary imports
import json
import zipfile

# Default name for mined data file in compressed archive
DATA_FILE: str = "mined_data.json"

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