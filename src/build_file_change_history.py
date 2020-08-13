#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

##########
# translates the flat/unstructured JSON commit data into a history of file changes
# the resulting graph is a series of DAG where each nodes has at most one parent and one child
##########

##########
# Import libraries
##########
import logging
import networkx as nx
import seaborn as sns
from collections import defaultdict
import time

def build_file_change_history(known_commits, file_change_history):

    
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `known_commits` : list of dicts, required, input of this function, commit data generated by perceval in the function get_commit.py
    `file_change_history` : networkx DiGraph, required, output of this function, empty container for the file change history 
 
    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """

    # store each filechange in each commit as a node in the graph
    for commit in known_commits:
        if 'files' in commit:
            for filechange in commit['files']:
                node_id = filechange["file"] + "_" + commit["commit"] # unique node identifier
                file_change_history.add_node(
                    node_id, # unique node identifier
                    unique_id = node_id, 
                    file = filechange["file"],
                    Author = commit["Author"],
                    Committer = commit["Commit"],
                    AuthorDate = commit["AuthorDate"],
                    CommitDate = commit["CommitDate"],
                    commit = commit["commit"]
                )
                # NOTE: For some reason it is not possible to retrieve the unique id of a node from networkx (at least I haven't found the way).
                #       As a consequence, I need to store the unique id as an attribute. That is a bit ugly and redundant...
                # TODO: Find a way to retrieve the ID of a networkx node.

                if "added" in filechange:
                    file_change_history.nodes[node_id]["added"] = filechange["added"]
                else:
                    print(f"Warning: missing file edition information (key 'added') for file {filechange['file']} in commit {commit['commit']}")
                if "removed" in filechange:
                    file_change_history.nodes[node_id]["removed"] = filechange["removed"]
                else:
                    print(f"Warning: missing file edition information (key 'removed') for file {filechange['file']} in commit {commit['commit']}")
                if "action" in filechange:
                     file_change_history.nodes[node_id]["action"] = filechange["action"]
                else:
                    print(f"Warning: missing file edition information (key 'action') for file {filechange['file']} in commit {commit['commit']}")
        else:
            logging.warning("warning: commit " + commit['commit'] + " has no attribute 'files'.")
            # TODO: investigate why some commits have no attribute 'file'      
 
    
    # Partition the unstuctured list of file changes.
    # Phe result is a dictionary of lists where keys are commited filenames
    # We use collections.defaultdict so we can use dict[key].append() even if key does not exist (a normal dict would throw a KeyError)
    partitionned_filechanges = defaultdict(list)
    for filechange_id in file_change_history.nodes:
        partitionned_filechanges[file_change_history.nodes[filechange_id]['file']].append(file_change_history.nodes[filechange_id])


    # colouring: define one colour for each unique filename
    # TODO: the following snippet is a duplicate from "build_commit_history.py". Consider making a function out of it.
    palette = sns.color_palette("hls", len(partitionned_filechanges.keys())) # returns a rgb tuple normalzed in [0,1]
    palette_html = list()
    for colour_tuple in palette: # convert the palette to HTML format
        html_colour_code = '#'
        for colour_code in colour_tuple:
            html_colour_code = html_colour_code + '%02x' % int(round(colour_code*256))
        palette_html.append(html_colour_code) 

    # connect nodes in sequences of file changes and apply colouring
    for i, sublist in enumerate(list(partitionned_filechanges.values())):
        
        # sort the list per timestamp
        sublist.sort(key=lambda x:time.mktime(time.strptime(x['AuthorDate'], '%a %b %d %H:%M:%S %Y %z'))) # example: Mon Mar 26 16:04:21 2018 +0100
        # TODO: for now we rely on AuthorDate for sorting the file change events. We need to check what would be the impact of using CommitDate instead.
        
        # connect the nodes two by two in the sorted sequence
        for j in range(1,len(sublist)):
            file_change_history.add_edge(
                sublist[j-1]['unique_id'],
                sublist[j]['unique_id'],
                colour = palette_html[i]
            )

        # apply colouring to nodes
        for node in sublist:
            node['colour'] = palette_html[i]


