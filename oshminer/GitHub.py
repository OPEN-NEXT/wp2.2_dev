#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

def make_GitHub_request(url: str, data: list) -> str: 
    print(f"Constructing an API request to GitHub for repository {url} for the following data {data}")