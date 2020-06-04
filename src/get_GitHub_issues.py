#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

# Given a GitHub repository URL (e.g. OPEN-NEXT/wp2.2_dev),
# retrieve all of its issues with metadata.

# Use the perceval library to access GitHub
from perceval.backends.core.github import GitHub
