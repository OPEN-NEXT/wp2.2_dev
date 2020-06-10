#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Gather parameters from commandline arguments and the configuration file to
# initialise the rest of the scripts in this repository.

import argparse
import json
import sys
from json.decoder import JSONDecodeError


def get_configuration() -> dict:
    """Initialise starting options for git-mining script

    Returns:
        dictionary: key-value pairs for file paths to configuration (key "config_file"), GitHub authentication token (key "auth_file"), directory for downloaded data (key "data_dir"), and list of repositories to mine (key "repo_file").
    """
    # Define commandline options
    parser = argparse.ArgumentParser(
        description="Mines metadata from GitHub repositories given a list.")
    parser.add_argument("-c", "--config_file", type=str, required=False,
                        help="Path to configuration file. Will override corresponding --auth and --repolist options.")
    parser.add_argument("-a", "--auth_token", type=str, required=False,
                        help="Path to GitHub personal authentication token file.")
    parser.add_argument("-d", "--data_dir", type=str, default="__DATA__", required=False,
                        help="Path to directory for storing downloaded data (which will be created if it doesn't exist).")
    parser.add_argument("-r", "--repo_file", type=str, default="repolist_example.csv", required=False, 
                        help="Path to CSV file containing list of repositories to mine.")
    # Get commandlines options
    parsed_config = parser.parse_args()

    # Create dictionary to hold options
    configuration: dict = dict()
    # Put user supplied options into the dictionary
    configuration["config_file"] = parsed_config.config_file
    configuration["auth_token"] = parsed_config.auth_token
    configuration["data_dir"] = parsed_config.data_dir
    configuration["repo_file"] = parsed_config.repo_file

    # Use configuration file if it is specified, overriding any existing options
    if (configuration["config_file"] == None) or (configuration["config_file"] == ""):
        pass
    else:
        custom_config = None
        try:
            with open(file=configuration["config_file"], mode="r") as config_file:
                try:
                    custom_config = json.load(config_file)
                except JSONDecodeError as json_error:
                    print(f"Error parsing configuration file:\n{json_error}", file=sys.stderr)
                    exit(1)
                del config_file
        except FileNotFoundError as not_found:
            print(f"Specified configuration file not found:\n{not_found}", file=sys.stderr)
        for key in custom_config.keys():
            try:
                configuration[key] # This will test if the key should exist
                configuration[key] = custom_config[key]
            except KeyError as key_error:  # Deal with undefined options
                print(
                    f"{key_error} option is not supported in configuration file.", file=sys.stderr)

    # Test for required options still missing (if so, complain)
    empty_options: list = [key for key, value in configuration.items() if key != "config_file" and (value == "" or value == None)]
    if len(empty_options) > 0:
        print("There are still required options missing:")
        for missing_item in empty_options:
            print(missing_item)
            print("Please try again, exiting.")
            exit(1)

    # Then put the authentication string into its own entry
    try:
        with open(configuration["auth_token"], mode="r") as token_file:
            token_file_lines = token_file.read().split(sep="\n")
            # Read first line of provided token file as authentication token string
            configuration["auth_token"] = token_file_lines[0]
            del token_file, token_file_lines
    except FileNotFoundError as token_file_error:
        print(f"Can't find GitHub API authentication token file.")
        print(token_file_error)
        exit(1)
    except Exception as other_error:
        print(f"Error accessing GitHub API authentication token file: \n {other_error}")
        exit(1)

    # Return a dictionary of initialisation options
    return configuration
