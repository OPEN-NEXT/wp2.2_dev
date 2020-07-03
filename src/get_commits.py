#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Get commits in a git repository.
# When two files are edited within the same commit, that counts as a connection
# between them in a downstream adjacency matrix.

##########
# Import libraries
##########

import os
import logging
from sys import stderr
from perceval.backends.core.git import Git
from perceval.errors import RepositoryError # To handle errors with repositories

##########
# Pull commits from a git repository
##########

def get_commits(username, reponame, commits, config):
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `username` : str, required
    `reponame` : str, required
    `commits` : list, required
 
    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """
    
    repo_URL = 'https://github.com/' + username + '/' + reponame
    logging.info('fetching info at ' + repo_URL)

     # checks whether the export dir exists and if not creates it # TODO: this is a code snippet we use three times, we should make a function out of it
    local_dir = os.path.join(config["data_dir"],'grimoire_dumps')
    if not os.path.isdir(local_dir):
        os.makedirs(local_dir)
    data_dump_path = os.path.join(local_dir, username + '-' + reponame)

    git = Git(repo_URL, data_dump_path)
    
    # `fetch()` gets commits from all branches by default.
    # It returns a list of dictionaries, where the `data` key in each
    # dictionary contains the actual metadata for each commit.
    # Other stuff are metadata about the perceval `fetch()` operation.
    try:
        repo_fetched = [commit for commit in git.fetch()]
        # Keep just commit `data`
        for commit_data in repo_fetched:
            commits.append(commit_data["data"])
    except RepositoryError as repo_error:
        logging.warning("Error with this repository: " + username + "/" + reponame, file=stderr)
        pass

        
    #
    # some code for exploring `test.json` which contains only
    # two items from the grimoirelab-toolkit Github repository
    # above
    #
    
    # # read in test file `test.json` with the two items
    # with open("test.json", "r") as testfile:
    #     testfile_content = testfile.read()
    #     testfile_commits = json.loads(testfile_content)
    
    # # get the first item which itself is in JSON,
    # # which is embodied as a dictionary in Python
    # testfile_commit_0 = testfile_commits[1]
    
    # # the "data" item in this dictionary is itself a dictionary
    # # and contains the actual commit metadata
    # testfile_commit_0["data"]
    
    # # for example, do this to get the timestamp and hash of the
    # # commit
    # testfile_commit_0["data"]["CommitDate"]
    # testfile_commit_0["data"]["commit"]
    # repo_URL = ""
