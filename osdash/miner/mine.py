#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import json
import sys

# Internal imports
if __name__ == "__main__":
    from adapters import GitHub, Wikifactory
else:
    from . adapters import GitHub, Wikifactory

# External imports
import pandas

STAGED_DATA: str = "./staged_data-example.json"

def mine(staged_data):
    mined_data: pandas.core.frame.DataFrame = staged_data
    return mined_data

def main():
    with open(STAGED_DATA) as json_file: 
        loaded_json = json.load(json_file)
        loaded_json: str = json.dumps(loaded_json)
    staged_data: pandas.core.frame.DataFrame = pandas.read_json(loaded_json, orient="columns")
    mined_data: pandas.core.frame.DataFrame = mine(staged_data)
    print(mined_data)

if __name__ == "__main__": 
    main()
    sys.exit(0)