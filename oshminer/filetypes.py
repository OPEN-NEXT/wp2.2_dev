#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

# 1. Categorised list of file extensions
# 
# Each category is a `list` and each extension should be in only one list.
# 
# Most extensions are from this paper: 
# Bonvoisin, J., Buchert, T., Preidel, M., & Stark, R. G. (2018). How 
# participative is open source hardware? Insights from online repository 
# mining. Design Science, 4(e19). https://doi.org/10.1017/dsj.2018.15
# 
# Extensions changed or not from that paper are marked in comments.
#
# 2. Additional file extension information
#
# `osh_file_types` is derived from a list of open source hardware file 
# extension information from the Open Source Ecology Germany CAD and PCB file 
# type metadata lists: 
# https://gitlab.com/OSEGermany/osh-file-types/

# Python Standard Library imports
import csv

#
# 1. Categorised list of file extensions
#

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

#
# 2. Additional file extension information
#

# Column mappings to shorter names
column_mappings: dict = {
    "File extension": "extension", 
    "File format [open|proprietary|unknown]": "format", 
    "Encoding [text|binary|both|unknown]": "encoding", 
    "Category [source|export]": "category"
}

# Read list of CAD files
with open("oshminer/osh-file-types/file_extension_formats-cad.csv", newline = '') as cad_formats_file: 
    cad_reader: csv.DictReader = csv.DictReader(cad_formats_file, delimiter=',')
    # Get column names, see: 
    # https://stackoverflow.com/a/28837325/186904 
    # https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
    cad_files: list = list(cad_reader)
# Rename `dict` keys for each entry for easier handling, see: 
# https://stackoverflow.com/a/16475444/186904
for column_name in list(column_mappings.keys()): 
    cad_files: list = [{column_mappings[column_name] if k == column_name else k:v for k,v in r.items()} for r in cad_files]

# Read list of PCB files
with open("oshminer/osh-file-types/file_extension_formats-pcb.csv", newline = '') as pcb_formats_file: 
    pcb_reader: csv.DictReader = csv.DictReader(pcb_formats_file, delimiter=',')
    # Get column names, see: 
    # https://stackoverflow.com/a/28837325/186904 
    # https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
    pcb_files: list = list(pcb_reader)
# Rename `dict` keys for each entry for easier handling, see: 
# https://stackoverflow.com/a/16475444/186904
for column_name in list(column_mappings.keys()): 
    pcb_files: list = [{column_mappings[column_name] if k == column_name else k:v for k,v in r.items()} for r in pcb_files]

# Combine CAD and PCB lists
osh_file_types: list = cad_files + pcb_files