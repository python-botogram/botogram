"""
    Tests for botogram/utils/calls.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.utils


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
