#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# Categorised list of file extensions
# Each category is a `list` and each extension should be in only one list.
# 
# Most extensions are from this paper: 
# Bonvoisin, J., Buchert, T., Preidel, M., & Stark, R. G. (2018). How 
# participative is open source hardware? Insights from online repository 
# mining. Design Science, 4(e19). https://doi.org/10.1017/dsj.2018.15
# 
# Extensions changed or not from that paper are marked in comments.

# Electronic CAD
ecad: list = [
    "brd", 
    "drl", 
    "dsn", 
    "fz", # added
    "fzz", 
    "gbl", 
    "gbo", 
    "gbp", 
    "gbr", 
    "gbs", 
    "gml", 
    "gpi", 
    "gtl", 
    "gto", 
    "gtp", 
    "gts", 
    "kicad_mod", 
    "kicad_pcb", 
    "kicad_pcb-bak", 
    "pcb", 
    "pde", 
    "sch"
]

# Mechanical CAD
mcad: list = [
    "123dx", 
    "3dm", 
    "art", 
    "blend", 
    "blend1", 
    "crv", 
    "dft", 
    "dra", 
    "dwf", 
    "dwg", 
    "easm", 
    "epf", 
    "fcmacro", 
    "fcstd", 
    "fcstd1", 
    "gcode", 
    "iam", 
    "idw", 
    "iges", 
    "igs", 
    "ipj", 
    "ipn", 
    "ipt", 
    "makerbot", 
    "mb", 
    "nc", 
    "obj", 
    "par", 
    "psm", 
    "scad", 
    "skp", 
    "sldasm", 
    "slddrw", 
    "sldprt", 
    "step", 
    "stl", 
    "stp", 
    "thing", 
    "vert", 
    "x_t", 
    "x3g"
]

# Image
image: list = [
    "ai", 
    "bmp", 
    "cdr", 
    "drawio", # added
    "dxf", 
    "eps", 
    "gif", 
    "ico", 
    "jpeg", 
    "jpg", 
    "odg", # added
    "png", 
    "psd", 
    "svg", 
    "tiff", 
    "xcf", 
    "xmp"
]

# Data (not originally a category in Bonvoisin et al. (2018))
data: list = [ 
    "csv", # moved from `document`
    "json", 
    "ods", # moved from `document`
    "xls", # moved from `document`
    "xlsx"# moved from `document`
]

# Document
document: list = [
    "bib", # added
    "docx", 
    "gdoc", 
    "htm", 
    "html", 
    "markdown", 
    "md", 
    "odt", 
    "odp", # added
    "pdf", 
    "rst", # added
    "rtf", 
    "shtml", 
    "tex", # added
    "txt", 
    "yaml" # added
]