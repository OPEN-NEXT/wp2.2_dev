#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import getopt
import networkx as nx
import json
from pyvis.network import Network

# import the necessary custom functions
# TODO: is there a way to use indirection to avoid repeating the same code again and again?
try:
    from get_Github_forks import get_Github_forks
except:
    print("Need `get_Github_forks.py`")
    exit(1)
try:
    from get_commits import get_commits
except:
    print("Need `get_commits.py`")
    exit(1)
try:
    from build_commit_history import build_commit_history
except:
    print("Need `get_commits.py`")
    exit(1)


def main():
    # get command line arguments
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'u:r:t:', [
                                           'user=', 'repo=', 'token='])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    # initialise the parameters to be found in the arguments
    username = ''
    repo = ''
    token_path = ''

    for option, argument in options:
        if option in ('-u', '--user'):
            username = argument
        if option in ('-r', '--repo'):
            repo = argument
        if option in ('-t', '--token'):
            token_path = argument
 
    # check whether all required parameters have been given as arguments and if not throw exception and abort
    if username == '':
        print ("Argument required: GitHub username. Type '-u <username>' in the command line")
        sys.exit(2)
    if repo == '':
        print ("Argument required: GitHub repository. Type '-r <filepath>' in the command line")
        sys.exit(2)
    if token_path == '':
        print ("Argument required: OAuth token file. Type '-t <directory path>' in the command line")
        sys.exit(2)

    print("User: " + username)
    print("Repository: " + repo)
    print("Token file: " + token_path)
    #
    # Get Github personal access token
    #

    auth = dict()

    try:
        with open(file=token_path, mode="r") as token_file:
            token_items = token_file.read().split(sep="\n")
            auth["login"] = token_items[0]
            auth["secret"] = token_items[1]
            del(token_file, token_items)
    except FileNotFoundError as token_error:
        print("Can't find or open Github API access token file.\n" + + str(token_error))
        exit(2)

    forks = list()
    forks.append({'user': username,
                'repo': repo,
                'parent_user': username,
                'parent_repo': repo})

    get_Github_forks(username=username, reponame=repo, forks=forks, auth=auth)

    print("There are " + str(forks.__len__()) + " forks of " + username + "/" + repo)

    # JB 2020 05 03 - BEGIN
    # Commented saving a json file with fork references
    # we don't need a file anymore since we used directly the fork references to fetch commits
    # forks_json = json.dumps(forks, sort_keys=True, indent=4)
    # output_file = repo + ".json"
    # save the Perceval docs to a file
    # with open(output_file, 'w') as f:
    #     f.write(forks_json)
    # JB 2020 05 03 - END

    known_commits = list() # compilation of all commits of all forks, without duplicates
    for fork in forks:
        print("retrieving commits in " + fork['user'] + "/" + fork['repo'])
        commits = list() # all commits of this fork
        get_commits(username=fork['user'], reponame=fork['repo'], commits=commits)
        known_commits_shas = [x['commit'] for x in known_commits]
        for commit in commits:
            if not commit['commit'] in known_commits_shas:
                known_commits.append(commit)
    
    output_JSON = '../__DATA__/JSON_commits/' + username + '-' + repo + '.json'
    # convert commits to a JSON string for export
    commits_JSON = json.dumps(known_commits, sort_keys=True, indent=4)
    # save the commits to a file
    with open(output_JSON, 'w') as f:
       f.write(commits_JSON)
    del f
    
    # JB 2020 05 03 - BEGIN
    # JB comment: is this to check whether the export was successful? Needed?
    # this reloads the commits from the exported file
    #with open(output_JSON, 'r') as f:
    #    content = f.read()
    #    commits = json.loads(content)
    # JB 2020 05 03 - END

    # recreate the 'network' view in GitHub (repo > insights > network)
    commit_history = nx.DiGraph() # netwrok is supposed to be a DAG (directed acyclic graph)
    build_commit_history(known_commits, commit_history)
            
    output_GML = '../__DATA__/commit_histories/' + username + '-' + repo + '.gml'
    nx.write_gml(commit_history, output_GML)
    
    # alternative to GML file: pyvis visualisation
    # alternative: 1 https://towardsdatascience.com/python-interactive-network-visualization-using-networkx-plotly-and-dash-e44749161ed7
    # alternative: 2 https://graph-tool.skewed.de/
    # alternative 3: vis.js from scratch https://github.com/marcin-kolda/py-graph-vis
    pyvis_network = Network(height="1000px", width="562px", bgcolor="#222222", font_color="white")
    pyvis_network.show_buttons(filter_=['layout'])
    pyvis_network.from_nx(commit_history)
    output_pyvis = '../__DATA__/commit_histories/' + username + '-' + repo + '.html'
    pyvis_network.save_graph(output_pyvis)
   
    
if __name__ == "__main__":
    main()
