#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Main package configuration file.

This is a Python file that specifies configuration options for the whole
package. Details of each configuration option are in the comments.

This file will be `import`ed by `__init__.py` to initialise the package.
"""

# Python Standard Library import(s)
import os

# Logging options

#
#  [logger configuration options go here e.g. log verbosity]
#

# Path to list of repositories to mine
REPOS_LIST: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), "OSH-repos.csv")

# Path to data output directory where mined data will be stored
OUTPUTS_PATH: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")