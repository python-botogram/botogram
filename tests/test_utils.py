"""
    Tests for botogram/utils.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.utils
import botogram.decorators


STRANGE_DOCSTRING = """ a


  b

"""


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


def test_format_docstr():
    # This docstring needs lots of cleanup...
    res = botogram.utils.format_docstr(STRANGE_DOCSTRING)
    assert res == "a\n\nb"

    # This instead should be left as it is
    ok = "a\nb"
    assert botogram.utils.format_docstr(ok) == ok


def test_docstring_of(bot):
    # This function will be used in the testing process
    def func():
        """docstring"""

    # Before everything, test with the default docstring
    assert botogram.utils.docstring_of(func) == "docstring"

    # Next try with an empty docstring
    func.__doc__ = ""
    assert botogram.utils.docstring_of(func) == "No description available."

    # And else try to use a custom function
    # This will also test if botogram.utils.format_docstr is called
    @botogram.decorators.help_message_for(func)
    def help_func():
        return STRANGE_DOCSTRING

    assert botogram.utils.docstring_of(func) == "a\n\nb"


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


def test_call():
    testfunc_called = 0

    # Just a test function
    def testfunc(a, b, c):
        nonlocal testfunc_called
        testfunc_called += 1

        assert a == 1
        assert b == 2
        assert c == 3

    # Call the function with the exact list of arguments
    botogram.utils.call(testfunc, a=1, b=2, c=3)
    assert testfunc_called == 1

    # Call the function with more arguments than the needed ones
    botogram.utils.call(testfunc, a=1, b=2, c=3, d=4)
    assert testfunc_called == 2

    # Call the function with less arguments than the needed ones
    with pytest.raises(TypeError):
        botogram.utils.call(testfunc, a=1, b=2)
    assert testfunc_called == 2


def test_call_with_wraps():
    mywrapper_called = False
    myfunc_called = False

    def myfunc(a, b):
        nonlocal myfunc_called
        myfunc_called = True

        assert a == 1
        assert b == 2

    @botogram.utils.wraps(myfunc)
    def mywrapper(c):
        nonlocal mywrapper_called
        mywrapper_called = True

        assert c == 3

        botogram.utils.call(myfunc, a=1, b=2, c=3)

    botogram.utils.call(mywrapper, a=1, b=2, c=3)
    assert mywrapper_called
    assert myfunc_called


def test_call_lazy_arguments():
    myfunc1_called = False
    myfunc2_called = False
    myarg_called = False

    def myfunc1(a):
        nonlocal myfunc1_called
        myfunc1_called = True

        assert a == 1

    def myfunc2(a, b):
        nonlocal myfunc2_called
        myfunc2_called = True

        assert a == 1
        assert b == 2

    def myarg():
        nonlocal myarg_called
        myarg_called = True

        return 2

    lazy = botogram.utils.CallLazyArgument(myarg)

    botogram.utils.call(myfunc1, a=1, b=lazy)
    assert myfunc1_called
    assert not myarg_called

    botogram.utils.call(myfunc2, a=1, b=lazy)
    assert myfunc2_called
    assert myarg_called
