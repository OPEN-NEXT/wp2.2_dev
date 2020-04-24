#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import sys
import getopt

import json

try:
    from get_Github_forks import get_Github_forks
except:
    print("Need `get_Github_forks.py`")
    exit(1)


def main():
    # get command line arguments
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'u:r:t', [
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
        print("Can't find or open Github API access token file.")
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

if __name__ == "__main__":
    main()
