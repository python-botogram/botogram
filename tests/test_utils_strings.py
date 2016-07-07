"""
    Tests for botogram/utils/strings.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

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
