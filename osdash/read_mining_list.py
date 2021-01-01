#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Import external modules
import pandas

def read_repo_list(path: str = "../data/OSH-repos-GitHub-test.csv") -> pandas.core.frame.DataFrame:
    """
    docstring
    """
    repo_list: pandas.core.frame.DataFrame = pandas.read_csv(path)

    # TODO: Basic input data validation happens here.

    return repo_list

my_repos = read_repo_list()

print("pause")