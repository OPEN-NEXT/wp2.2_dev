#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Given a GitHub repository URL (e.g. OPEN-NEXT/wp2.2_dev),
# retrieve all of its issues with metadata. Note that this includes
# pull requests.

# Use the perceval library to access GitHub.
from perceval.backends.core.github import GitHub

# Use perceval's GitHub() to dump issues data from repository.
repo_dump = GitHub(owner="OPEN-NEXT", repository="wp2.2_dev", api_token=["9dba7d2bc919139eb32f6cd67aedc7771cb229dc"], sleep_for_rate=True, sleep_time=300)

# Clean up the dumped data which results in a list that contains a "data"
# columns which contains the actual data on each issue.
issues_dump: list = [item for item in repo_dump.fetch()]

# Create a new list and append data from each issue to it.
issues_list: list = list()
for issue in issues_dump:
    issues_list.append(issue["data"])
# Sort this issues list by GitHub issue number. Note the use of a lambda 
# function, see here: https://docs.python.org/3/howto/sorting.html
issues_list = sorted(issues_list, key=lambda issue: issue["number"])
# Alternative sorting method with custom instead of lambda function.
# def get_issue_number (issue: dict):
#     return issue["number"]
# issues_list = sorted(issues_list, key=get_issue_number)