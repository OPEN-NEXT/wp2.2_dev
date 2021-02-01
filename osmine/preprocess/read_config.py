#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# TODO: Finish logging functionality

# Python Standard Library imports
import argparse
import logging
import os
import sys

# External imports
import yaml

# Default options
DEFAULT_REPO_LIST: str = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "input/OSH-repos.csv")
DEFAULT_DATA_DIR: str = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data")

# Function to process commandline and configuration file options
def read_config() -> dict:
    """Initialise starting options for git-mining script

    Returns:
        dictionary: key-value pairs for file paths to configuration (key "config_file"), 
        GitHub authentication token (key "GitHub_token"), 
        output directory for downloaded data (key "data_dir"), 
        list of repositories to mine (key "repo_list"), 
        log config (key "log_config"), 
        and if output directory should be created (key "create_data_dir").
    """
    #
    # Retrive configuration options
    #
    print("Reading configuration")
    print(os.path.abspath(__file__))

    # Get commandline options first
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Mines metadata from GitHub repositories given a list.")
    parser.add_argument("-c", "--config_file", type=str, required=False,
                        help="Path to configuration file. Will override corresponding --auth and --repolist options.")
    parser.add_argument("-t", "--GitHub_token", type=str, required=False,
                        help="Path to GitHub personal authentication token file.")
    parser.add_argument("-d", "--data_dir", type=str, required=False,
                        help="Output directory for storing downloaded data.")
    parser.add_argument("-r", "--repo_list", type=str, required=False, 
                        help="Path to CSV file containing list of repositories to mine.")
    parser.add_argument("--create_data_dir", type=bool, default=True, required=False,
                        help = "If data output directory doesn't exist, create it.")
    parsed_config: argparse.Namespace = parser.parse_args()

    # Create dictionary to hold mandatory options
    configuration: dict = dict()
    configuration["repo_list"] = DEFAULT_REPO_LIST
    configuration["GitHub_token"] = None
    configuration["data_dir"] = DEFAULT_DATA_DIR
    configuration["create_data_dir"] = None
    # Put commandline options into the dictionary
    configuration["config_file"] = parsed_config.config_file

    #
    # Apply configuration file first
    #

    if not(configuration["config_file"] == None):
        logging.info("Trying to parse configuration file:" + configuration["config_file"])
        # Start an empty configuration then populate from file
        config_file_options = None
        try:
            with open(file=configuration["config_file"], mode="r") as config_file:
                try:
                    config_file_options = yaml.safe_load(config_file)
                except yaml.YAMLError as yaml_error:
                    logging.critical(f"Error parsing configuration file: \n{yaml_error}")
                    sys.exit(1)
                del config_file
        except FileNotFoundError as not_found:
            logging.critical(f"Configuration file not found: {not_found}")
        else:
            # Apply options from configuration file
            for key in config_file_options.keys():
                try:
                    configuration[key] # Will throw KeyError exception if option isn't defined
                except KeyError as key_error: # Deal with undefined option
                    logging.warning(f"{key_error} option is not supported in configuration file.")
                else:
                    configuration[key] = config_file_options[key] # Only valid options will be used propogated
    
    #
    # Read environment variables
    #

    # Read GitHub token from environment variable if it is there
    # Reference: https://stackoverflow.com/q/40697845/186904
    if "GH_TOKEN" in os.environ:
        logging.info(f"Reading GitHub token from environment variable GH_TOKEN")
        configuration["GitHub_token"] = os.environ["GH_TOKEN"]

    #
    # Apply commandline arguments
    #

    # Commandline arguments would override anything in the configuration file
    # or environment variables

    if parsed_config.GitHub_token != None: 
        configuration["GitHub_token"] = parsed_config.GitHub_token
    if parsed_config.data_dir != None: 
        configuration["data_dir"] = parsed_config.data_dir
    if parsed_config.repo_list != None: 
        configuration["repo_list"] = parsed_config.repo_list
    if (parsed_config.create_data_dir != None) and (configuration["create_data_dir"] == None): 
        configuration["create_data_dir"] = parsed_config.create_data_dir


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
    # Process GitHub API token
    #

    # Put the authentication string into its own entry
    if not("GH_TOKEN" in os.environ):
        # I.e. Try to open token file if the token is not already read from environment
        try:
            with open(configuration["GitHub_token"], mode="r") as token_file:
                token_file_lines = token_file.read().split(sep="\n")
                # Read first line of provided token file as authentication token string
                configuration["GitHub_token"] = token_file_lines[0]
            del token_file, token_file_lines
        except FileNotFoundError as token_file_error:
            logging.critical(f"Can't find GitHub API authentication token file.")
            logging.critical(token_file_error)
            sys.exit(1)
        except Exception as other_error:
            logging.critical(f"Error accessing GitHub API authentication token file: {other_error}")
            sys.exit(1)

    # Check if GitHub authentication key string looks correct
    # AFAIK the token should be exactly 40 alphanumeric characters
    try:
        assert (configuration["GitHub_token"].isalnum() and len(configuration["GitHub_token"]) == 40)
    except AssertionError:
        logging.critical("GitHub authentication key doesn't look right: {}".format(configuration["GitHub_token"]))
        logging.critical("It should be a 40-character alphanumeric string. Please try again.")
        sys.exit(1)
    else:
        logging.debug("GitHub authentication key looks OK.")
    
    #
    # Prepare output data directory `data_dir`
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

    # Return a dictionary of initialisation options
    return configuration

# If this file is run on its own, usually in a debugging context, then main() 
# will run: 
def main(): 
    print(f"In read_config.py's main()")
    print(f"Current workding directory is: ")
    print(os.getcwd())
    config: dict = read_config()
    print(f"main() done")

if __name__ == "__main__":
    main()
    sys.exit(0)