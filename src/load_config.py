#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os


# Does what is said on the tin: it loads the config (from the ".config" file to be stored in the working directory, usually the same directory where the script is stored)

def load_default(): # Loads default values / TODO: there may be a more elegant way to do this
    config = {}
    config["config_file_path"] = ".config"
    config["data_dir_path"] = "../__DATA__"
    config["token_file_path"] = ".token"
    return config

def load_config():
    
    # first we load the default config
    config = load_default()
    
    # then we load the user/custom config, if there is some
    if os.path.isfile(config["config_file_path"]):
        with open(config["config_file_path"], 'r') as f :
            custom_config = json.load(f)
        del f
        

        # then we override the default config with the custom config 
        for key in custom_config.keys():
            if key in config.keys():
                config[key] = custom_config[key]
            else:
                print("Warning: config parameter '" + key + "' not supported") # TODO: replace with proper exception handling


    return config