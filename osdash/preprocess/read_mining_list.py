#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""[summary]

Describe format of the CSV file with required columns, headers, data types,
and how each cell should be formatted, etc.

Acceptable items in column `repo_platform` are...

Note: The `notes` columns is optional and completely ignored.

Returns:
    pandas.core.frame.DataFrame: [description]
"""

# Python Standard Library imports
import os
import sys
import urllib

# External imports
import numpy
import pandas

# Define the required columns of input CSV file being explicit about data type
REQUIRED_COLUMNS: dict = {
    "project": str,
    "repo_url": str,
    "repo_platform": str
}

def read_repo_list(path: str) -> pandas.core.frame.DataFrame:
    """
    docstring
    """

    #
    # Import list of repositories to mine
    #

    # Get a list of the names of the required columns
    column_names: list = list(REQUIRED_COLUMNS.keys())

    # Only proceed if CSV file exists
    if not os.path.exists(path): 
        print(f"ERROR: Can't find CSV at: {path}", file=sys.stderr)
        exit(1)
    
    # Import data into Pandas dataframe using `dtype=REQUIRED_COLUMNS` to be
    # explicit about expected data types for columns
    repo_list: pandas.core.frame.DataFrame = pandas.read_csv(path, 
    dtype=REQUIRED_COLUMNS)

    #
    # Validate and clean imported data
    #

    # Check if the required CSV headers are present
    for header in column_names: 
        if not (header in repo_list.columns.values): 
            # Stop execution if a required header is missing
            print(f"ERROR: Required column heading '{header}' not in {path}", file=sys.stderr)
            exit(1)

    # Keep only the required columns
    repo_list = repo_list[column_names]
    
    # Drop rows with empty cells including those with empty strings
    # Reference: https://stackoverflow.com/a/29314880/
    # Convert empty strings to NaN type first: 
    repo_list.replace("", numpy.nan, inplace=True)
    # Then drop rows with NaNs
    repo_list.dropna(inplace=True)

    # Drop duplicate rows with identical `repo_url`s
    repo_list.drop_duplicates(subset="repo_url", inplace=True)

    # Basic sanity check on each repository's URL so that they contain at least
    # scheme (e.g. "https://") and netloc (e.g. "opennext.eu") defined in 
    # `min_url_attributes`.
    # Reference: https://stackoverflow.com/a/36283503/
    min_url_attributes: list = ["scheme", "netloc"]
    for url in repo_list["repo_url"]: 
        tokens: urllib.parse.ParseResult = urllib.parse.urlparse(url)
        if not all([getattr(tokens, attr) for attr in min_url_attributes]): 
            # Stop execution if an URL doesn't look right
            print(f"ERROR: {url} does not appear to be a useable URL", file=sys.stderr)
            exit(1)
        else: 
            pass

    return repo_list

def main():
    """
    This `main()` will be run if this file is run on its own, presumably
    when debugging it.
    Use the environment variable `REPO_PATH` to specify the CSV file to read
    from.
    """
    if "REPO_PATH" in os.environ: 
        REPO_PATH: str = os.environ["REPO_PATH"]
        my_repos: pandas.core.frame.DataFrame = read_repo_list(path=REPO_PATH)
    else: 
        print(f"Please set path to repository list CSV with REPO_PATH environment variable", file=sys.stderr)
    pass

if __name__ == "__main__": 
    main()