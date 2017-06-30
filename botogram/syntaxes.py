# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
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

import re

from . import utils


_markdown_re = re.compile(r".*("
                          r"\*(.*)\*|"
                          r"_(.*)_|"
                          r"\[(.*)\]\((.*)\)|"
                          r"`(.*)`|"
                          r"```(.*)```"
                          r").*")

_html_re = re.compile(r".*("
                      r"<b>(.*)<\/b>|"
                      r"<strong>(.*)<\/strong>|"
                      r"<i>(.*)<\/i>|"
                      r"<em>(.*)<\/em>|"
                      r"<a\shref=\"(.*)\">(.*)<\/a>|"
                      r"<code>(.*)<\/code>|"
                      r"<pre>(.*)<\/pre>"
                      r").*")


def is_markdown(message):
    """Check if a string is actually markdown"""
    # Don't mark part of URLs or email addresses as Markdown
    message = utils.strip_urls(message)

    return bool(_markdown_re.match(message.replace("\n", "")))


def is_html(message):
    """Check if a string is actually HTML"""
    # Here URLs are not stripped because no sane URL contains HTML tags in it,
    # and for a few cases the speed penality is not worth
    return bool(_html_re.match(message.replace("\n", "")))


def guess_syntax(message, provided):
    """Guess the right syntax for a message"""
    if provided is None:
        if is_markdown(message):
            return "Markdown"
        elif is_html(message):
            return "HTML"
        else:
            return None

    if provided in ("plain",):
        return None
    elif provided in ("md", "markdown", "Markdown"):
        return "Markdown"
    elif provided in ("html", "HTML"):
        return "HTML"
    else:
        raise ValueError("Invalid syntax: %s" % provided)
