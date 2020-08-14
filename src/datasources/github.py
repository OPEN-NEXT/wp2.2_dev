#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys

# Read GitHub authorisation token from file

def read_token(token_path: str) -> str:
    try:
        with open(token_path, mode="r") as token_file:
            token_file_lines = token_file.read().split(sep="\n")
            # Read first line of provided token file as authentication token string
            auth_token = token_file_lines[0]
        del token_file, token_file_lines
    except FileNotFoundError as token_file_error:
        print(f"Can't find GitHub API authentication token file.", file=sys.stderr)
        sys.exit(1)
    except Exception as other_error:
        print(f"Error accessing GitHub API authentication token file: {other_error}", file=sys.stderr)
        sys.exit(1)
    else: 
        # Check if authentication key string looks correct
        # AFAIK the token should be exactly 40 alphanumeric characters
        try:
            assert (auth_token.isalnum() and len(auth_token) == 40)
        except AssertionError:
            print("GitHub authentication key doesn't look right: {}".format(auth_token), file=sys.stderr)
            print("It should be a 40-character alphanumeric string. Please try again.", file=sys.stderr)
            sys.exit(1)
        else:
            print("GitHub authentication key looks OK.", file=sys.stderr)
            return auth_token