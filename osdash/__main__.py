#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This is the dashboard's main module.
It defines a main function to be executed, representing execution of the
whole package. This function is high-level and calls other internal modules
that contain the actual plumbing.
"""

# Python Standard Library import(s)
import sys

# External import(s)

# Internal import(s)
import preprocess

# High-level `main()` that spells out data-mining logic

def main():
    """
    docstring
    """
    print(f"Start of main() in __main__.py")
    # Read configuration file
    configuration: dict = preprocess.read_config()

    # Run pre-processor that reads list of repositories to mine and existing data
    #staging_data = 

    sys.exit(0)

if __name__ == "__main__":
    main()