#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt

import json

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

    forks_json = json.dumps(forks, sort_keys=True, indent=4)

    output_file = repo + ".json"

    # save the Perceval docs to a file
    with open(output_file, 'w') as f:
        f.write(forks_json)

    for fork in forks:
        print("retrieving commits in " + fork['user'] + "/" + fork['repo'])
        get_commits(fork['user'], fork['repo'])

if __name__ == "__main__":
    main()
