#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Python Standard Library import(s)

import json
import zipfile
# import zlib

# Prepare some data
data: dict = {
    "common_name": "Brongersma's short-tailed python",
    "scientific_name": "Python brongersmai",
    "length": 290
}

# Save data to a JSON file
# with open("data.json", "w", encoding="utf-8") as output_JSON_file: 
#     json.dump(data, output_JSON_file, ensure_ascii=False, indent=4)

#
# Try `zlib`
#

# Open saved JSON then compress it
# with open ("data.json", "r", encoding="utf-8") as input_JSON_file: 
#     data: dict = json.load(input_JSON_file)
#     # Data needs to be saved as bytes to be compressed
#     data_bytes: bytes = json.dumps(data, indent=4).encode("utf-8")
#     compressed_data = zlib.compress(data_bytes, level=zlib.Z_BEST_COMPRESSION)
#     with open ("compressed_zlib.zip" , "wb") as output_zlib_file: 
#         output_zlib_file.write(compressed_data)

#
# Try `zipfile`
#

# Open a `ZipFile`
with zipfile.ZipFile("compressed_data_ZipFile.zip", mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file: 
    dumped_JSON = json.dumps(data, ensure_ascii=False, indent=4)
    zip_file.writestr("data.json", data=dumped_JSON)
    zip_file.testzip()

# Read from the created `ZipFile`
with zipfile.ZipFile("compressed_data_ZipFile.zip", mode="r") as zip_file: 
    with zip_file.open("data.json") as JSON_file: 
        extracted_JSON = json.load(JSON_file)
        print(type(extracted_JSON))