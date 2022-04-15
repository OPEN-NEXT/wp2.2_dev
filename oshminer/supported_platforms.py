#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports
import os
import sys

# Internal imports
import oshminer.GitHub
import oshminer.Wikifactory

# Set Wikifactory base URL for projects
# Looks for the `WIF_BASE_URL` environment variable, and if not found, default to: 
# `wikifactory.com`
# See: 
# https://www.twilio.com/blog/environment-variables-python
WIF_BASE_URL: str = os.environ.get("WIF_BASE_URL", "wikifactory.com")
print(f"Wikifactory base URL: {WIF_BASE_URL}", file=sys.stderr)

# Supported hosting platforms as a dictionary of their domains, which are 
# matched to names of internal functions that construct API requests to the 
# associated platforms.
# `repo_urls` in the request body needs to include one of these domains.
supported_domains: dict = { 
    "github.com": oshminer.GitHub.make_GitHub_request, 
    WIF_BASE_URL: oshminer.Wikifactory.make_Wikifactory_request
}