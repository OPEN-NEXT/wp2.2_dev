#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Recursively find all forks of a Github repository

# Import `requests` library for API calls
try:
    import requests
# If library not present, throw exception
except ImportError:
    print("Need `requests` library available")
    exit(1)

def get_Github_forks(username, reponame, forks, auth=None):
    """
    TODO: Add docstring. See: https://realpython.com/documenting-python-code/
    TODO: Implement recursion argument, default to False.

    Parameters
    ==========

    `username` : str, required
    `reponame` : str, required
    `forks` : list, required
    `auth` : dict, optional

    Raises
    ======

    NotImplementedError
        If no sound is set for the animal or passed in as a
        parameter.
    """

    page = 1  # Track page number of Github API response
    while True:
        print("Finding forks of "
              + username
              + "/"
              + reponame
              + " page "
              + str(page))
        r = None
        request_url = "https://api.github.com/repos/{}/{}/forks".format(
            username, reponame)
        if auth is None:
            # Use the `params` argument to get specific `page` of results from
            # API which produces `?page=*` after `request_url`
            r = requests.get(url=request_url,
                             params={"page": page})
        else:
            r = requests.get(url=request_url,
                             params={"page": page},
                             headers={"Authorization": "token " + auth})
        j = r.json()
        r.close()

        if "message" in j:
            print("username: {}, repository: {}".format(username, reponame))
            print(j['message']
                  + " "
                  + j['documentation_url'])
            if str(j['message']) == "Not Found":
                break
            else:
                exit(1)

        if len(j) == 0:
            break
        else:
            page += 1

        for item in j:
            forks.append({'user': item['owner']['login'],
                          'repo': item['name'],
                          'parent_user': username,
                          'parent_repo': reponame})

            if item["forks"] > 0:
                if auth is None:
                    get_Github_forks(username=item['owner']['login'],
                                     reponame=item['name'],
                                     forks=forks)
                else:
                    get_Github_forks(username=item['owner']['login'],
                                     reponame=item['name'],
                                     forks=forks,
                                     auth=auth)