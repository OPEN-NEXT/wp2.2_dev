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

def build_commit_history(known_commits, commit_history):

    
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `known_commits` : list of dicts, required
    `commit_history` : nx DiGraph, required
 
    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """
    
    # first pass: add all nodes
    
    for commit in known_commits:
    # add the current node to the network
        commit_history.add_node(commit['commit'][:7],
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
            commit_history.add_edge(parent_sha[:7], commit['commit'][:7])
            # TODO implement correct branch naming in the network graph