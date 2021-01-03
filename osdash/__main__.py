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
import pandas

# Internal import(s)
if __name__ == "__main__": 
    import preprocess
else:
    from . preprocess import read_config, stage_data

# High-level `main()` that spells out data-mining logic

def main():
    """
    docstring
    """
    print(f"Start of main() in __main__.py")

    #
    # Read configuration file
    #

    configuration: dict = preprocess.read_config()

    #
    # Stage existing data
    #

    # This includes reading from list of repositories to mine

    staged_data: pandas.core.frame.DataFrame = preprocess.stage_data(configuration["repo_list"])

    print(f"foobar")

if __name__ == "__main__":
    main()
    sys.exit(0)