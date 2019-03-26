#!/usr/bin/env python3
# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

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
copyright = "2015-2019 The Botogram Authors"
author = "Botogram-dev"

version = "0.6"
release = "0.6"

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
