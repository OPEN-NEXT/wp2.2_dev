# [license info here]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Get commits in a git repository.
# When two files are edited within the same commit, that counts as a connection
# between them in a downstream adjacency matrix.

##########
# Import libraries
##########

from perceval.backends.core.git import Git
import json

##########
# Pull commits from a git repository
##########

repo_URL = 'https://github.com/chaoss/grimoirelab-toolkit'
local_path = './chaoss-grimoirelab-toolkit'
output_JSON = './grimoirelab-git.json'

git = Git(repo_URL, local_path)

# `fetch()` gets commits from all branches by default.
# It returns a list of dictionaries, where the `data` key in each
# dictionary contains the actual metadata for each commit.
# Other stuff are metadata about the perceval `fetch()` operation.
repo_fetched = [commit for commit in git.fetch()]

# Print the contents of those commits
for c in repo_fetched:
    print(c["data"])
del c

# Keep just commit `data`
commits = []
for commit_data in repo_fetched:
    commits.append(commit_data["data"])

##########
# Export commits to a JSON file
##########

# convert commits to a JSON string for export
commits_JSON = json.dumps(commits, sort_keys=True, indent=4)

# save the commits to a file
with open(output_JSON, 'w') as f:
    f.write(commits_JSON)
del f

# this reloads the commits from the exported file
#with open(output_JSON, 'r') as f:
#    content = f.read()
#    commits = json.loads(content)

##########
# Get file chamges in each commit
##########

file_changes = []
for commit in commits:
    file_changes.append({
        "Author": commit["Author"],
        "CommitDate": commit["CommitDate"],
        "commit": commit["commit"],
        "files": commit["files"],
        "no_files": len(commit["files"])
        })
















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
repo_URL = ""
