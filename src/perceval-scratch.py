#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from perceval.backends.core.git import Git
from perceval.backends.core.github import GitHub
import json
import requests
import itertools

#
# using data from perceval command
#

'''
    install perceval and then parse the output
    pip install perceval
    perceval git https://github.com/chaoss/grimoirelab-toolkit --json-line
    > /tmp/test-command.txt
'''

in_file = 'grimoirelab-toolkit.txt'
out_file = 'grimoirelab-toolkit.json'

commits = []

with open(in_file, 'r') as f:
    for line in f:
        commits.append(line)

with open(out_file, 'w') as f:
    f.write(json.dumps(commits, sort_keys=True, indent=4))

with open(out_file) as str_data:
    print(str_data)
    json_data = json.load(str_data)

#
# getting data via perceval in Python
#

url = 'https://github.com/chaoss/grimoirelab-toolkit'
local_path = './chaoss-grimoirelab-toolkit'
output_file = './grimoirelab-git.json'

git = Git(url, local_path)

commits = [commit for commit in git.fetch()]

dumped = json.dumps(commits, sort_keys=True, indent=4)

# save the Perceval docs to a file
with open(output_file, 'w') as f:
    f.write(dumped)

# load the Perceval docs from a file
with open(output_file, 'r') as f:
    content = f.read()
    commits = json.loads(content)

for c in commits:
    print(c)

#
# some code for exploring `test.json` which contains only
# two items from the grimoirelab-toolkit Github repository
# above
#

# read in test file `test.json` with the two items
with open("test.json", "r") as testfile:
    testfile_content = testfile.read()
    testfile_commits = json.loads(testfile_content)

# get the first item which itself is in JSON,
# which is embodied as a dictionary in Python
testfile_commit_0 = testfile_commits[1]

# the "data" item in this dictionary is itself a dictionary
# and contains the actual commit metadata
testfile_commit_0["data"]

# for example, do this to get the timestamp and hash of the
# commit
testfile_commit_0["data"]["CommitDate"]
testfile_commit_0["data"]["commit"]

#
# getting Github issues with perceval
#

# pull all issues for a Github repository
git = GitHub(owner="chaoss", repository="grimoirelab-toolkit")
git_issues = [issue for issue in git.fetch()]

# look at one of the issues
git_issues[23]["data"]
# still need to look at how the order of the issues here link to that on Github

# put issues into a JSON object
git_issues_json = json.dumps(git_issues, sort_keys=True, indent=4)
# write JSON to file
with open("git_issues_json.json", 'w') as f:
    f.write(git_issues_json)