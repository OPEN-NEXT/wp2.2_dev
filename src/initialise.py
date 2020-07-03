#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Gather parameters from commandline arguments and the configuration file to
# initialise the rest of the scripts in this repository.

import argparse
import csv
import json
import os
import sys
import unicodedata
import logging
from logging.config import dictConfig

from json.decoder import JSONDecodeError

def initialise_options() -> dict:
    """Initialise starting options for git-mining script

    Returns:
        dictionary: key-value pairs for file paths to configuration (key "config_file"), 
        GitHub authentication token (key "auth_token"), 
        output directory for downloaded data (key "data_dir"), 
        list of repositories to mine (key "repo_list"), 
        log config (key "log_config"), 
        and if output directory should be created (key "create_data_dir").
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
    parser.add_argument("-r", "--repo_list", type=str, default="repolist_example.csv", required=False, 
                        help="Path to CSV file containing list of repositories to mine.")
    parser.add_argument("--create_data_dir", type=bool, default=True, required=False,
                        help = "If data output directory doesn't exist, create it.")
    parsed_config = parser.parse_args()

    # Create dictionary to hold mandatory options
    configuration: dict = dict()
    # Put user supplied options into the dictionary
    configuration["config_file"] = parsed_config.config_file
    configuration["auth_token"] = parsed_config.auth_token
    configuration["data_dir"] = parsed_config.data_dir
    configuration["repo_list"] = parsed_config.repo_list
    configuration["create_data_dir"] = parsed_config.create_data_dir
    configuration["log_config"] = None

    #
    # Apply configuration file if it is supplied
    #

    if (configuration["config_file"] == None) or (configuration["config_file"] == ""):
        logging.info("No configuration file specified.")
    else:
        logging.info("Trying to parse configuration file:" + configuration["config_file"])
        # Start an empty configuration then populate from file
        custom_config = None
        try:
            with open(file=configuration["config_file"], mode="r") as config_file:
                try:
                    custom_config = json.load(config_file)
                except JSONDecodeError as json_error:
                    logging.critical(f"Error parsing configuration file: {json_error}")
                    sys.exit(1)
                del config_file
        except FileNotFoundError as not_found:
            logging.critical(f"Specified configuration file not found: {not_found}")
        else:
            # Override commandline options with configuration file
            for key in custom_config.keys():
                try:
                    configuration[key] # Will throw KeyError exception if option isn't defined
                except KeyError as key_error: # Deal with undefined option
                    logging.warning(f"{key_error} option is not supported in configuration file.")
                else:
                    configuration[key] = custom_config[key] # Only valid options will be used propogated


    #
    # Test for required options still missing (if so, complain)
    #

    # Use a list comprehension that will include items still empty or `None`
    empty_options: list = [key for key, value in configuration.items() if key != "config_file" and (value == "" or value == None)]
    if len(empty_options) > 0:
        logging.critical("There are still required options missing:")
        for missing_item in empty_options: # List missing items
            logging.critical(missing_item)
            logging.critical("Please try again, exiting.")
        sys.exit(1)

    #
    # Handle log level option
    #

    # Apply user-supplied config, if supplied. If not, continue with default settings
    if "log_config" in configuration:
        try:
            dictConfig(configuration["log_config"])
        except Exception as log_config_error:
            logging.critical(f"Error parsing log config: {log_config_error}")
            sys.exit(1)

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
        logging.critical(f"Can't find GitHub API authentication token file.")
        logging.critical(token_file_error)
        sys.exit(1)
    except Exception as other_error:
        logging.critical(f"Error accessing GitHub API authentication token file: {other_error}")
        sys.exit(1)
    else: 
        # Check if authentication key string looks correct
        # AFAIK the token should be exactly 40 alphanumeric characters
        try:
            assert (configuration["auth_token"].isalnum() and len(configuration["auth_token"]) == 40)
        except AssertionError:
            logging.critical("GitHub authentication key doesn't look right: {}".format(configuration["auth_token"]))
            logging.critical("It should be a 40-character alphanumeric string. Please try again.")
            sys.exit(1)
        else:
            logging.debug("GitHub authentication key looks OK.")
    
    #
    # Create ouput data directory `data_dir`
    #

    # If `data_dir` doesn't exist, create it unless explicitly disabled
    try:
        assert os.path.isdir(configuration["data_dir"]), "Output directory '{}' doesn't exist.".format(configuration["data_dir"])
    except AssertionError as no_data_dir:
        logging.error(no_data_dir)
        if configuration["create_data_dir"]:
            logging.info("Creating output data directory:")
            logging.info(os.getcwd() + "/" + configuration["data_dir"])
            os.makedirs(name=configuration["data_dir"])
        else:
            logging.critical("Option 'create_data_dir' is {}, exiting.".format(configuration["create_data_dir"]))
            sys.exit(1)

    #
    # Process input list of repositories (`repo_list`) to mine
    #

    # Check if `repo_list` exists and parses correctly
    try:
        assert os.path.isfile(configuration["repo_list"]), "Error accessing repository list: {}".format(configuration["repo_list"])
    except AssertionError as no_repo_list:
        logging.critical(no_repo_list)
        sys.exit(1)
    else:
        try:
            with open(configuration["repo_list"], newline="") as repo_file:
                repo_csv = csv.DictReader(repo_file)
                repo_list: list = list()
                for row in repo_csv:
                    repo_list.append(row)
            del repo_file, repo_csv
        except Exception as read_csv_error: # TODO: Make Exception more specific
            logging.critical(f"Error parsing repository list: {read_csv_error}")
            sys.exit(1)
    # Check repository list format
    bad_rows: list = list() # Create an empty list to record list items in wrong format
    for row in repo_list: # TODO: More efficient way to check than go through each list item
        try: # Make sure "owner" and "repo" fields consistently exist
            assert "owner" in row and "repo" in row, "Repository list CSV file needs field names 'owner' and 'row'"
        except AssertionError as fieldname_error:
            logging.critical(fieldname_error)
            sys.exit(1)
        else:
            # Record which items don't have exactly two items, one each for "owner" and "repo", 
            # plus if there are empty (None) cells
            if len(row) != 2 or None in row.values():
                bad_rows.append(row)
    try: # If there are bad items in repository list, print them and exit
        assert len(bad_rows) == 0, "Some rows in repository list have problems: "
    except AssertionError as item_error:
        logging.critical(item_error)
        for bad_row in bad_rows:
            logging.critical(bad_row.values()) # TODO: Make this more human-readable
        sys.exit(1)
            
    # TODO: Remove duplicate entries in `repo_list`
    # Put `repo_list` into `configuration`
    configuration["repo_list"] = repo_list

    # Return a dictionary of initialisation options
    return configuration
