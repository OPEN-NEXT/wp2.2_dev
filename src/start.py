#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

################################################################################################################################################
################################################################################################################################################
# Imports 
################################################################################################################################################
################################################################################################################################################

# standard libraries
import argparse
import json
import os
import sys

import networkx as nx
import json

# import the necessary custom functions
try:
    from initialise import initialise_options
    from get_Github_forks import get_Github_forks
    from get_commits import get_commits
    from build_commit_history import build_commit_history
    from build_file_change_history import build_file_change_history
    from build_committer_graph import build_committer_graph
    from build_committer_graph import export_committer_graph
    from load_config import load_config
except ImportError as import_error:
    print(
        f"Error importing required module(s):\n{import_error}", file=sys.stderr)
    exit(1)
except:
    print("Error when importing required modules.", file=sys.stderr)
    exit(1)

# functions 

def build_export_file_path(dir_path, filename):
    # checks if the dir_path exists and if not create it
    # then returns the (now valid) file path 
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    return os.path.join(
        dir_path, filename)

################################################################################################################################################
################################################################################################################################################
# Initialisation 
################################################################################################################################################
################################################################################################################################################

def main():
    # Get commandline and configuration file options
    configuration: dict = initialise_options()

################################################################################################################################################
################################################################################################################################################
# Get (all forks of) all forks 
################################################################################################################################################
################################################################################################################################################

    forks = list()
    forks.append({'user': username,
                  'repo': repo,
                  'parent_user': username,
                  'parent_repo': repo})

    get_Github_forks(username=username, reponame=repo, forks=forks, auth=auth)

    print("There are " + str(forks.__len__()) +
          " forks of " + username + "/" + repo)

################################################################################################################################################
################################################################################################################################################
# get all commits from all previously fetched forks 
################################################################################################################################################
################################################################################################################################################

    known_commits = list()  # compilation of all commits of all forks, without duplicates
    for fork in forks:
        print("retrieving commits in " + fork['user'] + "/" + fork['repo'])
        commits = list()  # all commits of this fork
        get_commits(
            username=fork['user'], reponame=fork['repo'], commits=commits, config=configuration)
        known_commits_shas = [x['commit'] for x in known_commits]
        for commit in commits:
            if not commit['commit'] in known_commits_shas:
                known_commits.append(commit)
    # netwrok is supposed to be a DAG (directed acyclic graph)
    build_commit_history(known_commits, commit_history)

    # stringize the non string node attributes not supported by GrapML
    for node in commit_history.nodes():
        commit_history.nodes[node]['refs'] = str(
            commit_history.nodes[node]['refs'])
        commit_history.nodes[node]['parents'] = str(
            commit_history.nodes[node]['parents'])
    
    # export the file commit history as GraphML
    output_GraphML = build_export_file_path(
        os.path.join(config["data_dir_path"], 'commit_histories'), 
        username + '-' + repo + '.GraphML') 
    nx.write_graphml(commit_history, output_GraphML)

################################################################################################################################################
################################################################################################################################################
# build history of file changes based on the previously previously fetched (flat) list of commits
################################################################################################################################################
################################################################################################################################################

    # network is supposed to be a DAG (directed acyclic graph)
    file_change_history = nx.DiGraph() 
    build_file_change_history(known_commits, file_change_history)
    
    # export the file change history as GraphML
    output_GraphML = build_export_file_path(
        os.path.join(config["data_dir_path"], 'file_change_histories'), 
        username + '-' + repo + '.GraphML') 
    nx.write_graphml(file_change_history, output_GraphML)

################################################################################################################################################
################################################################################################################################################
# build committer graph based on the previously previously generated file change history
################################################################################################################################################
################################################################################################################################################

    committer_graph = nx.MultiDiGraph() 
    build_committer_graph(file_change_history, committer_graph)
    
    # export the file committer graph as GraphML
    output_GraphML = build_export_file_path(
        os.path.join(config["data_dir_path"], 'committer_graphs'), 
        username + '-' + repo + '.GraphML') 
    nx.write_graphml(committer_graph, output_GraphML)

    JSON_string = json.dumps(nx.node_link_data(committer_graph), sort_keys=True, indent=4)
    output_JSON = build_export_file_path(
        os.path.join(config["data_dir_path"], 'committer_graphs'), 
        username + '-' + repo + '.json') 
    with open(output_JSON, 'w') as f:
       f.write(JSON_string)
    del f

    output_VISJS = os.path.join(os.path.join(config["data_dir_path"], 'committer_graphs'), username + '-' + repo + '.html')
    export_committer_graph(committer_graph, output_VISJS)
    
if __name__ == "__main__":
    main()
