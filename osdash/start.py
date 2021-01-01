#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

################################################################################################################################################
################################################################################################################################################
# Imports 
################################################################################################################################################
################################################################################################################################################

# standard libraries
import json
import os
import sys
import logging
import json
from dateutil import parser

import networkx as nx
import pandas as pd
import numpy as np


# default logging configuration
# needs to be on top of the code, otherwise all calls to logging.<something> happening
# before the custom confifuration is loaded or in case no custom configuration is
# given would be ignored
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# import the necessary custom functions
try:
    from initialise import initialise_options
    from get_Github_forks import get_Github_forks
    from get_commits import get_commits
    from build_commit_history import build_commit_history
    from build_file_change_history import build_file_change_history
    from build_committer_graph import build_committer_graph
    from build_committer_graph import export_committer_graph
except ImportError as import_error:
    logging.error(
        f"Error importing required module(s):\n{import_error}", file=sys.stderr)
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

    #
    # The rest of the script acts on each item in the list of git repositories to mine
    #

    logging.info(f"Start processing the {len(configuration['repo_list'])} repositories passed on")
    for repository in configuration["repo_list"]:
        logging.info(f"--- Start processing repository {repository['owner']}/{repository['repo']} ---")
        username = repository["owner"]
        repo = repository["repo"]

        ########################################################################################################################################
        ########################################################################################################################################
        # Get (all forks of) all forks 
        ########################################################################################################################################
        ########################################################################################################################################

        # Initialise an empty list of forks
        forks = list()
        forks.append({'user': username,
                      'repo': repo,
                      'parent_user': username,
                      'parent_repo': repo})

        get_Github_forks(username=username, reponame=repo, forks=forks, auth=configuration["auth_token"])

        logging.info(f"{str(forks.__len__()-1)} forks found")

        ########################################################################################################################################
        ########################################################################################################################################
        # get all commits from all previously fetched forks 
        ########################################################################################################################################
        ########################################################################################################################################

        known_commits: list = list()  # compilation of all commits of all forks, without duplicates
        known_commits_shas: list = list() # for easier access later
        time_stamps: list = list() # so we can index commits per date

        for fork in forks:
            commits = list()  # all commits of this fork
            get_commits(
                username=fork['user'], reponame=fork['repo'], commits=commits, config=configuration)
            for commit in commits:
                if not commit['commit'] in known_commits_shas:
                    known_commits.append(commit)
                    known_commits_shas.append(commit['commit'])
                    time_stamps.append(
                        np.datetime64(
                            parser.parse(commit['CommitDate'])
                        )
                    )

        # create a panda.DataFrame with the known_commits data
        sorted_commits = pd.DataFrame(
            list(zip(known_commits_shas, known_commits)), 
            columns=['sha','commit_data'],
            index=pd.DatetimeIndex(time_stamps)
        )
        logging.info(f"{str(known_commits.__len__())} commits found")
        del known_commits, known_commits_shas, time_stamps

        # convert commits to a JSON string for export
        commits_JSON = json.dumps(
            sorted_commits['commit_data'].values.tolist(), 
            sort_keys=True, 
            indent=4
        )
    
        # save the commits to a file
        output_JSON = build_export_file_path(
            os.path.join(configuration["data_dir"], 'JSON_commits'), 
            username + '-' + repo + '.json') 
        with open(output_JSON, 'w') as f:
            f.write(commits_JSON)
        del f

        # filter by time window 
        ######################################################################################
        # Arbitrary filter after April 2020 / for a test
        #sorted_commits = sorted_commits[sorted_commits.index > '2020-07']

        ########################################################################################################################################
        ########################################################################################################################################
        # buid the commit history based on the previously fetched (flat) list of commits
        ########################################################################################################################################
        ########################################################################################################################################

        # recreate the 'network' view in GitHub (repo > insights > network)
        # network is supposed to be a DAG (directed acyclic graph)
        commit_history = nx.DiGraph()
        build_commit_history(sorted_commits['commit_data'].values.tolist(), commit_history)

        # stringize the non string node attributes not supported by GrapML
        for node in commit_history.nodes():
            commit_history.nodes[node]['refs'] = str(
                commit_history.nodes[node]['refs'])
            commit_history.nodes[node]['parents'] = str(
                commit_history.nodes[node]['parents'])

        logging.info(f"Commit history built with {len(commit_history.nodes())} nodes and {len(commit_history.edges())} edges")

        # export the file commit history as GraphML
        output_GraphML = build_export_file_path(
            os.path.join(configuration["data_dir"], 'commit_histories'), 
            username + '-' + repo + '.GraphML') 
        nx.write_graphml(commit_history, output_GraphML)

        ################################################################################################################################################
        ################################################################################################################################################
        # build history of file changes based on the previously previously fetched (flat) list of commits
        ################################################################################################################################################
        ################################################################################################################################################

        # network is supposed to be a DAG (directed acyclic graph)
        file_change_history = nx.DiGraph() 
        build_file_change_history(sorted_commits['commit_data'].values.tolist(), file_change_history)
    
        logging.info(f"File change history built with {len([c for c in nx.connected_components(file_change_history.to_undirected())])} files and {len(file_change_history.edges())} file changes")

        # export the file change history as GraphML
        output_GraphML = build_export_file_path(
            os.path.join(configuration["data_dir"], 'file_change_histories'), 
            username + '-' + repo + '.GraphML') 
        nx.write_graphml(file_change_history, output_GraphML)

        ################################################################################################################################################
        ################################################################################################################################################
        # build committer graph based on the previously previously generated file change history
        ################################################################################################################################################
        ################################################################################################################################################

        committer_graph = nx.MultiDiGraph() 
        build_committer_graph(file_change_history, committer_graph)
    
        logging.info(f"Commiter graph built with {len(committer_graph.nodes())} unique committers")

        # export the file committer graph as GraphML
        output_GraphML = build_export_file_path(
            os.path.join(configuration["data_dir"], 'committer_graphs'), 
            username + '-' + repo + '.GraphML') 
        nx.write_graphml(committer_graph, output_GraphML)

        JSON_string = json.dumps(nx.node_link_data(committer_graph), sort_keys=True, indent=4)
        output_JSON = build_export_file_path(
            os.path.join(configuration["data_dir"], 'committer_graphs'), 
            username + '-' + repo + '.json') 
        with open(output_JSON, 'w') as f:
           f.write(JSON_string)
        del f

        output_VISJS = os.path.join(os.path.join(configuration["data_dir"], 'committer_graphs'), username + '-' + repo + '.html')
        export_committer_graph(committer_graph, output_VISJS)
    
if __name__ == "__main__":
    main()
