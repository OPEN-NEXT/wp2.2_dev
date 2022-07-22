#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

class BadGitHubTokenError(Exception): 
    pass

class BadRepoError(Exception): 
    pass

class BadWIFAPIError(Exception):
    pass