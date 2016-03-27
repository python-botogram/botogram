#!/usr/bin/env python3
"""
    botogram documentation"s config file

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""
import sys
import os
import shlex

import pietroalbini_sphinx_themes

sys.path.append(os.path.abspath('_ext'))

extensions = []
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "botogram"
copyright = "2015-2016 Pietro Albini"
author = "Pietro Albini"

version = "0.2"
release = "0.2"

language = None

exclude_patterns = ["_build"]

#pygments_style = "botogramext.BotogramStyle"

todo_include_todos = False


## HTML output

html_theme = "botogram"
html_theme_path = ["_themes", pietroalbini_sphinx_themes.themes_path()]
html_static_path = ["_static"]

html_sidebars = {
    "**": ["links.html"],
}
#html_additional_pages = {}
#html_domain_indices = True
#html_use_index = True
#html_split_index = False
#html_show_sourcelink = True
#html_show_sphinx = True
#html_show_copyright = True
#html_search_language = "en"
#html_search_options = {"type": "default"}
#html_search_scorer = "scorer.js"

htmlhelp_basename = "botogramdoc"


## Latex output

latex_elements = {
#   "papersize": "letterpaper",
#   "pointsize": "10pt",
#   "preamble": "",
#   "figure_align": "htbp",
}

latex_documents = [
  (master_doc, "botogram.tex", "botogram Documentation",
   "Pietro Albini", "manual"),
]

#latex_logo = None
#latex_use_parts = False
#latex_show_pagerefs = False
#latex_show_urls = False
#latex_appendices = []
#latex_domain_indices = True


## Manpages output

man_pages = [
    (master_doc, "botogram", "botogram Documentation",
     [author], 1)
]
#man_show_urls = False


## Texinfo output

texinfo_documents = [
  (master_doc, "botogram", "botogram Documentation",
   author, "botogram", "One line description of project.",
   "Miscellaneous"),
]
#texinfo_appendices = []
#texinfo_domain_indices = True
#texinfo_show_urls = "footnote"
#texinfo_no_detailmenu = False
