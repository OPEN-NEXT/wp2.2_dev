#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports

# External imports
import pandas

def Wikifactory(repo_list: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    docstring
    """
    print(f"Begin Wikifactory adapter")
    mined_data: pandas.core.frame.DataFrame = repo_list

    return mined_data