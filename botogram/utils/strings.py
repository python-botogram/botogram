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
