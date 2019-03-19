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

import botogram.utils


def test_strip_urls():
    # Standard HTTP url
    assert botogram.utils.strip_urls("http://www.example.com") == ""

    # Standard HTTPS url
    assert botogram.utils.strip_urls("https://www.example.com") == ""

    # HTTP url with dashes in the domain (issue #32)
    assert botogram.utils.strip_urls("http://www.ubuntu-it.org") == ""

    # HTTP url with a path
    assert botogram.utils.strip_urls("http://example.com/~john/d/a.txt") == ""

    # Standard email address
    assert botogram.utils.strip_urls("john.doe@example.com") == ""

    # Email address with a comment (+something)
    assert botogram.utils.strip_urls("john.doe+botogram@example.com") == ""

    # Email address with subdomains
    assert botogram.utils.strip_urls("john.doe@something.example.com") == ""

    # Email address with dashes in the domain name (issue #32)
    assert botogram.utils.strip_urls("pietroalbini@ubuntu-it.org") == ""


def test_usernames_in():
    assert botogram.utils.usernames_in("Hi, what's up?") == []
    assert botogram.utils.usernames_in("Hi @johndoe!") == ["johndoe"]

    multiple = botogram.utils.usernames_in("Hi @johndoe, I'm @pietroalbini")
    assert multiple == ["johndoe", "pietroalbini"]

    command = botogram.utils.usernames_in("/say@saybot I'm @johndoe")
    assert command == ["johndoe"]

    email = botogram.utils.usernames_in("My address is john.doe@example.com")
    assert email == []

    username_url = botogram.utils.usernames_in("http://pwd:john@example.com")
    assert username_url == []
