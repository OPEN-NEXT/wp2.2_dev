#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

import oshminer.GitHub
import oshminer.Wikifactory

# Supported hosting platforms as a dictionary of their domains, which are 
# matched to names of internal functions that construct API requests to the 
# associated platforms.
# `repo_urls` need to include one of these domains.
supported_domains: dict = { 
    "github.com": oshminer.GitHub.make_GitHub_request, 
    "wikifactory.com": oshminer.Wikifactory.make_Wikifactory_request
}