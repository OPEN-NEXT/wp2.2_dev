#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

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


import networkx as nx
import json

# initialize default logger
# this needs to be at the top so 
from logging.config import dictConfig
dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s', 
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers' : {
            'default': {
                'level': 'INFO', 
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            }
    }, 
    'loggers': {
            '__main__': { # logging from this module will be logged in VERBOSE level
                'handlers' : ['default'], 
                'level': 'INFO', 
                'propagate': False,
            },
    },
    'root': {
            'level': 'INFO',
            'handlers': ['default']
    },
})
# about logging: 
#   https://gist.github.com/delicb/4540990#file-other-py-L3
#   https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules


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

    for repository in configuration["repo_list"]:
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

        logging.info("There are " + str(forks.__len__()) +
              " forks of " + username + "/" + repo)

        ########################################################################################################################################
        ########################################################################################################################################
        # get all commits from all previously fetched forks 
        ########################################################################################################################################
        ########################################################################################################################################

        known_commits = list()  # compilation of all commits of all forks, without duplicates
        for fork in forks:
            logging.info("retrieving commits in " + fork['user'] + "/" + fork['repo'])
            commits = list()  # all commits of this fork
            get_commits(
                username=fork['user'], reponame=fork['repo'], commits=commits, config=configuration)
            known_commits_shas = [x['commit'] for x in known_commits]
            for commit in commits:
                if not commit['commit'] in known_commits_shas:
                    known_commits.append(commit)
    
        # convert commits to a JSON string for export
        commits_JSON = json.dumps(known_commits, sort_keys=True, indent=4)
    
        # save the commits to a file
        output_JSON = build_export_file_path(
            os.path.join(configuration["data_dir"], 'JSON_commits'), 
            username + '-' + repo + '.json') 
        with open(output_JSON, 'w') as f:
            f.write(commits_JSON)
        del f

        ########################################################################################################################################
        ########################################################################################################################################
        # buid the commit history based on the previously fetched (flat) list of commits
        ########################################################################################################################################
        ########################################################################################################################################

        # recreate the 'network' view in GitHub (repo > insights > network)
        # network is supposed to be a DAG (directed acyclic graph)
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
        build_file_change_history(known_commits, file_change_history)
    
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
