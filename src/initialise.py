#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Gather parameters from commandline arguments and the configuration file to
# initialise the rest of the scripts in this repository.

import argparse
import json
import os
import sys
from json.decoder import JSONDecodeError
from sys import stderr
from warnings import warn


def get_configuration() -> dict:
    """Initialise starting options for git-mining script

    Returns:
        dictionary: key-value pairs for file paths to configuration (key "config_file"), GitHub authentication token (key "auth_file"), directory for downloaded data (key "data_dir"), and list of repositories to mine (key "repo_file").
    """
    #
    # Retrive configuration options
    #

    # Get commandlines options first
    parser = argparse.ArgumentParser(
        description="Mines metadata from GitHub repositories given a list.")
    parser.add_argument("-c", "--config_file", type=str, required=False,
                        help="Path to configuration file. Will override corresponding --auth and --repolist options.")
    parser.add_argument("-a", "--auth_token", type=str, required=False,
                        help="Path to GitHub personal authentication token file.")
    parser.add_argument("-d", "--data_dir", type=str, default="__DATA__", required=False,
                        help="Output directory for storing downloaded data.")
    parser.add_argument("-r", "--repo_file", type=str, default="repolist_example.csv", required=False, 
                        help="Path to CSV file containing list of repositories to mine.")
    parser.add_argument("--force_create_dir", type=bool, default=True, required=False,
                        help = "If data output directory doesn't exist, create it.")
    parsed_config = parser.parse_args()

    # Create dictionary to hold options
    configuration: dict = dict()
    # Put user supplied options into the dictionary
    configuration["config_file"] = parsed_config.config_file
    configuration["auth_token"] = parsed_config.auth_token
    configuration["data_dir"] = parsed_config.data_dir
    configuration["repo_file"] = parsed_config.repo_file
    configuration["create_data_dir"] = parsed_config.force_create_dir

    #
    # Apply configuration file if it is supplied
    #

    if (configuration["config_file"] == None) or (configuration["config_file"] == ""):
        print("No configuration file specified.")
    else:
        print("Trying to parse configuration file: \n" + configuration["config_file"])
        # Start an empty configuration then populate from file
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
        else:
            # Override commandline options with configuration file
            for key in custom_config.keys():
                try:
                    configuration[key] # Will throw KeyError exception if option doesn't/shouldn't exist
                except KeyError as key_error:  # Deal with undefined option
                    warn(message=f"{key_error} option is not supported in configuration file.", category=SyntaxWarning)
                else:
                    configuration[key] = custom_config[key] # This way, only valid options will be used


    #
    # Test for required options still missing (if so, complain)
    #

    # Use a list comprehension that will include items still empty or `None`
    empty_options: list = [key for key, value in configuration.items() if key != "config_file" and (value == "" or value == None)]
    if len(empty_options) > 0:
        print("There are still required options missing:", file=sys.stderr)
        for missing_item in empty_options: # List missing items
            print(missing_item, file=sys.stderr)
            print("Please try again, exiting.", file=sys.stderr)
            exit(1)

    #
    # Process GitHub API token
    #

    # Put the authentication string into its own entry
    try:
        with open(configuration["auth_token"], mode="r") as token_file:
            token_file_lines = token_file.read().split(sep="\n")
            # Read first line of provided token file as authentication token string
            configuration["auth_token"] = token_file_lines[0]
            del token_file, token_file_lines
    except FileNotFoundError as token_file_error:
        print(f"Can't find GitHub API authentication token file.", file=sys.stderr)
        print(token_file_error)
        exit(1)
    except Exception as other_error:
        print(f"Error accessing GitHub API authentication token file: \n{other_error}", file=sys.stderr)
        exit(1)
    else: 
        # Check if authentication key string looks correct
        # AFAIK the token should be exactly 40 alphanumeric characters
        try:
            assert (configuration["auth_token"].isalnum() and len(configuration["auth_token"]) == 40)
        except AssertionError:
            print("GitHub authentication key doesn't look right:\n{}".format(configuration["auth_token"]), file=stderr)
            print("It should be a 40-character alphanumeric string. Please try again.", file=stderr)
            exit(1)
        else:
            print("GitHub authentication key looks OK.")
    
    #
    # Create ouput data directory `data_dir`
    #

    # If `data_dir` doesn't exist, create it unless explicitly disabled
    try:
        assert os.path.isdir(configuration["data_dir"]), "Output directory '{}' doesn't exist.".format(configuration["data_dir"])
    except AssertionError as no_data_dir:
        print(no_data_dir)
        if configuration["create_data_dir"]:
            print("Creating output data directory:")
            print(os.getcwd() + configuration["data_dir"])
            os.makedirs(name=configuration["data_dir"])
        else:
            print("Option 'create_data_dir' is {}, exiting.".format(configuration["create_data_dir"]))
            exit(1)


    # TODO: Check if `repo_file` exists, looks right, and parses correctly

    # Return a dictionary of initialisation options
    return configuration
