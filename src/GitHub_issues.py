#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Given a GitHub repository URL (e.g. OPEN-NEXT/wp2.2_dev),
# retrieve all of its issues with metadata. Note that this includes
# pull requests.

import itertools
import json

# Use the perceval library to access GitHub.
from perceval.backends.core.github import GitHub
import networkx as nx

#owner: str = "OPEN-NEXT"
owner: str = "safecast"
#owner: str = "OpenROV"
#repo: str = "wp2.2_dev"
repo: str = "bGeigieNanoKit"
#repo: str = "openrov-hardware"
tokens: list = [""]


def get_issues(owner: str, repo: str, tokens: list) -> list:
    # Use perceval's `GitHub()` to dump issues data from repository.
    repo_dump = GitHub(owner=owner, repository=repo,
                       api_token=tokens, sleep_for_rate=True, sleep_time=300)

    # Clean up the dumped data which results in a list that contains a "data"
    # column which contains the actual data on each issue.
    issues_dump: list = [item for item in repo_dump.fetch()]

    # Create a new list and append data from each issue to it.
    issues_list: list = list()
    for issue in issues_dump:
        issues_list.append(issue["data"])
    # Sort this issues list by GitHub issue number. Note the use of a lambda
    # function, see here: https://docs.python.org/3/howto/sorting.html
    issues_list: list = sorted(issues_list, key=lambda issue: issue["number"])
    # # Alternative sorting method with custom instead of lambda function.
    # def get_issue_number (issue: dict):
    #     return issue["number"]
    # issues_list = sorted(issues_list, key=get_issue_number)

    # Add repository information to list.
    for issue in issues_list:
        issue.update({"owner": owner, "repo": repo})

    return issues_list


def add_participant(username: str, participants):
    """Internal function to append new participants

    Args:
        username (str): [description]
        participants (networkx.classes.graph.Graph or list): [description]

    Raises:
        TypeError: If `participants` is not a NetworkX graph or list
    """
    if isinstance(participants, nx.classes.graph.Graph):
        if username not in participants.nodes():
            participants.add_node(username, name=username, weight=0)
        # The following adds 1 weight to a user node whenever they interact with an issue, 
        # which could be opening an issue, commenting, or reacting.
        participants.nodes[username]["weight"] += 1
    elif isinstance(participants, list):
        if username not in participants:
            participants.append(username)
    else:
        raise TypeError("Issue participants argument type {} not supported".format(str(type(participants))))


GitHub_issues: list = get_issues(owner=owner, repo=repo, tokens=tokens)

# Keep only issues with comments
#issues_commented: list = [issue for issue in GitHub_issues if (issue["comments"] > 0)]
# Keep issues with comments or reactions (to the original post)
GitHub_issues_with_interactions: list = [issue for issue in GitHub_issues if (issue["comments"] > 0 or len(issue["reactions_data"]) >0)]

# Initialise an empty NetworkX graph
GitHub_issues_graph = nx.Graph(name="GitHub issues interaction graph")

for issue in GitHub_issues_with_interactions:
    # Create an empty list of users of this issue
    issue_users: list = list()

    #
    # 1. Add all participating users to a list
    #

    # 1a. Start by processing the issue's original post
    
    # Add its author to the list of users
    add_participant(issue["user"]["login"], issue_users)
    # If this author is no in the graph, add them to it
    add_participant(issue["user"]["login"], GitHub_issues_graph)
    # Process reactions to the original post and add users/interactions as needed
    for reaction in issue["reactions_data"]:
        # Add reaction's author to graph if they are not in it
        add_participant(reaction["user"]["login"], GitHub_issues_graph)
        # Add reaction's author to `issue_users`
        add_participant(reaction["user"]["login"], issue_users)

    # 1b. Process comments

    # Get all users who commented and reacted to comments
    for comment in issue["comments_data"]:
        # If commenter is not in graph, add them
        add_participant(comment["user"]["login"], GitHub_issues_graph)
        # If commenter is not in list of users of this issue, add them
        add_participant(comment["user"]["login"], issue_users)
        # If reactor to comment is not in graph, add them
        for reaction in comment["reactions_data"]:
            # Add reaction's author to graph if they are not in it
            add_participant(reaction["user"]["login"], GitHub_issues_graph)
            # Add reaction's author to `issue_users`
            add_participant(reaction["user"]["login"], issue_users)
    
    #
    # 2. Add interactions to graph
    #

    # We now have a list of all participants in this issue.
    # Add edges in the graph pairwise for all of them.

    # Get a list of all pairwise interactions (i.e. edges) to add
    new_edges = list(itertools.combinations(issue_users, r=2))
    
    # Add the edges, and if they already exist, then add to their weights
    for new_edge in new_edges:
        # If this edge doesn't exist, add it
        if GitHub_issues_graph.get_edge_data(new_edge[0], new_edge[1]) == None:
            GitHub_issues_graph.add_edge(new_edge[0], new_edge[1], weight=0)
        # In any case, add weight to the edge
        GitHub_issues_graph[new_edge[0]][new_edge[1]]["weight"] += 1
    pass

    


# in `my_issues`:
# Only issues x where my_issues[x]["comments"] > 0 have comments
#

pass

# Export GraphML
nx.write_graphml(GitHub_issues_graph, "GitHub_issues.GraphML")

# Export visualisation
# load the visjs template into a string
with open('visjs_template.html', 'r') as f:
    html_string = f.read()

# generate a string with js code including networkx data to concatenate with the visjs template
js_string = []
js_string.append("<script type='text/javascript'>\r\n")
js_string.append("imported_data = ")
js_string.append(json.dumps(nx.node_link_data(GitHub_issues_graph), sort_keys=True, indent=4))
js_string.append("\r\n</script>\r\n")

with open("GitHub_issues.html", 'w') as f:
    f.write(''.join(js_string) + html_string)
del f

pass
