#! [license info here]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########
# generates a network where each node is a committer and edges weights are the number of files they commonly edited
##########

##########
# Import libraries
##########
import networkx as nx
import seaborn as sns
from collections import Counter

def build_committer_graph(file_change_history, committer_graph):

    
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `file_change_history` : networkx DiGraph, required, input of this function, generated in "build_file_change_history.py"
    `committer_graph` : networkx DGraph, required, output of this function, empty container for the committer graph
 
    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """

    # step 1: generate nodes in the graph. Nodes are authors
    ######################################################################################
    # TODO: for now we rely on "Author" for identifying the authorship of the file changes
    # We need to check what would be the impact of using "Committer" instead.

    # get list with all authors
    # casting the list of authors as a set removes all duplicates
    authors = list(set([file_change_history.nodes[nodeID]['Author'] for nodeID in file_change_history.nodes()]))
    
    # get the number of times each author made a file change event
    filechanges = Counter(list(([file_change_history.nodes[nodeID]['Author'] for nodeID in file_change_history.nodes()])))

    for author in authors:
        committer_graph.add_node(
            author,
            weight = filechanges[author])


    # step 2: generate edges. Edges are common interactions between authors
    ######################################################################################
    # Parse all edges in the file change graph. 
    # Edges link together to subsequent file change events on a same file. 
    # If the committers of the file change events are different, we record an interaction between the committers
    for edge in file_change_history.edges:
        
        # networkx edges are two-element lists storing the ids of both linked nodes
        # edge[0] is the "from"/parent
        # edge[0] is the "to"/child
        # to retrieve the data associated with the node "from", we need to use graph.nodes[edge[0]]
        parent_node = file_change_history.nodes[edge[0]]
        child_node = file_change_history.nodes[edge[1]]

        # if the file changes represented by the parent and the child nodes have ben authored by different authors
        # then we add this interaction in the committer graph
        if parent_node["Author"] != child_node["Author"]:
            if committer_graph.get_edge_data(parent_node["Author"], child_node["Author"]) == None:
                # if there isn't any recorded interaction yet (get_edge_data returns None), we add an edge and initialise the weight to 1
                committer_graph.add_edge(parent_node["Author"], child_node["Author"], weight = 1)
            else:
                # if is already a recorded interaction, we increment the recorded weight
                # there is a recorded interaction if get_edge_data returns {0 {'weight': <weight>}}
                # the {0 ...} is because we use a MulitDiGraph, so get_edge_data returns a dict of links instead of one link
                committer_graph[parent_node["Author"]][child_node["Author"]][0]['weight'] = \
                    committer_graph[parent_node["Author"]][child_node["Author"]][0]['weight'] + 1