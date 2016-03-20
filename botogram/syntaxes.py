"""
    botogram.syntaxes
    Definition of the different message syntaxes

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

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
