#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import json
import zipfile

# Filename of mined data file that will be compressed
DATA_FILE: str = "mined_data.json"

def save_mined_data(path: str, mined_data: list):
    """
    docstring
    """
    # Export mined data as JSON file

    # Save output JSON file in a compressed archive with `zipfile` module
    with zipfile.ZipFile(path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file: 
        dumped_JSON: str = json.dumps(mined_data, ensure_ascii=False, indent=4)
        zip_file.writestr(DATA_FILE, data=dumped_JSON)
        # Test integrity of compressed archive
        zip_file.testzip()
    
    # Just save the JSON file with no compression
    # with open(file=path, mode="w", encoding="utf-8") as output_file:
    #     json.dump(mined_data, output_file, ensure_ascii=False, indent=4)