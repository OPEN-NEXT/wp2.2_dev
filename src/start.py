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

# custom functions
try:
    from get_Github_forks import get_Github_forks
    from get_commits import get_commits
    from build_commit_history import build_commit_history
    from build_file_change_history import build_file_change_history
    from build_committer_graph import build_committer_graph
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
    # get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, required=True)
    parser.add_argument("-r", "--repo", type=str, required=True)
    arguments = parser.parse_args()

    print(
        f"Will mine from this GitHub repo: {arguments.user}/{arguments.repo}")

    # initialise the parameters to be found in the arguments
    username = arguments.user
    repo = arguments.repo

    # load configuration file
    config = load_config()
    #
    # Get Github personal access token
    #

    auth = dict()

    try:
        with open(file=config["token_file_path"], mode="r") as token_file:
            token_items = token_file.read().split(sep="\n")
            auth["login"] = token_items[0]
            auth["secret"] = token_items[1]
            del token_file, token_items
    except FileNotFoundError as token_error:
        print("Can't find or open Github API access token file.\n" + str(token_error))
        exit(2)

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
            username=fork['user'], reponame=fork['repo'], commits=commits, config=config)
        known_commits_shas = [x['commit'] for x in known_commits]
        for commit in commits:
            if not commit['commit'] in known_commits_shas:
                known_commits.append(commit)
    
    # convert commits to a JSON string for export
    commits_JSON = json.dumps(known_commits, sort_keys=True, indent=4)
    
    # save the commits to a file
    output_JSON = build_export_file_path(
        os.path.join(config["data_dir_path"], 'JSON_commits'), 
        username + '-' + repo + '.json') 
    with open(output_JSON, 'w') as f:
        f.write(commits_JSON)
    del f

################################################################################################################################################
################################################################################################################################################
# buid the commit history based on the previously fetched (flat) list of commits
################################################################################################################################################
################################################################################################################################################

    # recreate the 'network' view in GitHub (repo > insights > network)
    # netwrok is supposed to be a DAG (directed acyclic graph)
    commit_history = nx.DiGraph()
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

    committer_graph = nx.Graph() 
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
    
if __name__ == "__main__":
    main()
