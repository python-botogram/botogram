"""
    botogram.syntaxes
    Definition of the different message syntaxes

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re


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
    return bool(_markdown_re.match(message))


def is_html(message):
    """Check if a string is actually HTML"""
    return bool(_html_re.match(message))


def guess_syntax(message, provided):
    """Guess the right syntax for a message"""
    if provided is None:
        if is_markdown(message):
            return "Markdown"
        elif is_html(message):
            return "HTML"
        else:
            return None

    if provided in ("md", "markdown", "Markdown"):
        return "Markdown"
    elif provided in ("html", "HTML"):
        return "HTML"
    else:
        raise ValueError("Invalid syntax: %s" % provided)
