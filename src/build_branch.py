#! [license info here]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########
# Import libraries
##########

# import networkx as nx


##########
# TODO: what does the function do
##########

def build_branch(known_commits, network):

    
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `username` : dict, required
    `reponame` : list of dicts, required
    `commits` : nx DiGraph, required
 
    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """
    
    # first pass: add all nodes
    
    for commit in known_commits:
    # add the current node to the network
        network.add_node(commit['commit'][:7],
                   commit=commit['commit'],
                   Author=commit['Author'],
                   AuthorDate=commit['AuthorDate'],
                   Commit=commit['Commit'],
                   CommitDate=commit['CommitDate'],
                   message=commit['message'],
                   )    
        
    # second pass: create links
    for commit in known_commits:
        # link the commit with their parents
        for parent_sha in commit['parents']:
            network.add_edge(parent_sha[:7], commit['commit'][:7])
            # TODO implement correct branch naming in the network graph