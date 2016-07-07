"""
    botogram.utils.strings
    Utilities for strings

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re


# URLs regex created by http://twitter.com/imme_emosol

_username_re = re.compile(r"\@([a-zA-Z0-9_]{5}[a-zA-Z0-9_]*)")
_command_re = re.compile(r"^\/[a-zA-Z0-9_]+(\@[a-zA-Z0-9_]{5}[a-zA-Z0-9_]*)?$")
_email_re = re.compile(r"[a-zA-Z0-9_\.\+\-]+\@[a-zA-Z0-9_\.\-]+\.[a-zA-Z]+")
_url_re = re.compile(r"https?://(-\.)?([^\s/?\.#]+\.?)+(/[^\s]*)?")


def strip_urls(string):
    """Strip URLs and emails from a string"""
    string = _url_re.sub("", string)
    string = _email_re.sub("", string)
    return string


def usernames_in(message):
    """Return all the matched usernames in the message"""
    # Don't parse usernames in the commands
    if _command_re.match(message.split(" ", 1)[0]):
        message = message.split(" ", 1)[1]

    # Strip email addresses from the message, in order to avoid matching the
    # user's domain. Also strip URLs, in order to avoid usernames in them.
    message = strip_urls(message)

    results = []
    for result in _username_re.finditer(message):
        if result.group(1):
            results.append(result.group(1))

    return results
