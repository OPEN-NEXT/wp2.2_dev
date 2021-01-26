#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This is the dashboard's main data-mining module.
It defines a main function to be executed, representing execution of the
whole package. This function is high-level and calls other internal modules
that contain the actual plumbing.
"""

# Python Standard Library imports
import pathlib
import sys

# External imports
import dash
import ipywidgets

# Workaround because for some reason internal imports can't be found once the 
# Dash app starts running:
sys.path.append(str(pathlib.Path(__file__).parent))
# Internal imports
import dash_app
import preprocess

# Some constants

# Default location for mined data JSON file
DATA_DIR: str = "./data"
DATA_FILE: str = "mined_data.zip"
# Form mined data file path
data_path: pathlib.Path = pathlib.Path(DATA_DIR) / pathlib.Path(DATA_FILE)

#
# Stage data mined from repositories
#

staged_data: list = preprocess.stage_data(str(data_path))

#
# Derive metrics
# 

# Note: Each item in this dictionary is a Pandas dataframe
derived_data: dict = preprocess.get_metrics(staged_data)

#
# Create Dash app
#

app: dash.Dash = dash_app.create_app(data=derived_data)

if __name__ == "__main__":
    #
    # Run Dash app server
    #
    app.run_server(debug=True, port=21110)