#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import json

def save_mined_data(path: str, mined_data: list):
    """
    docstring
    """
    # Export mined data as JSON file
    # TODO: Consider compressing the output to save disk space???
    
    with open(file=path, mode="w", encoding="utf-8") as output_file:
        json.dump(mined_data, output_file, ensure_ascii=False, indent=4)