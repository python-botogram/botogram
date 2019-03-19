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

import pickle

import pytest


def test_calling_functions(frozenbot):
    subset_called = False
    all_called = False

    # A subset of the arguments
    def subset(bot, a):
        nonlocal subset_called
        subset_called = True

        assert a == "foo"
        assert bot == frozenbot

    # All the arguments
    def all(bot, a, shared, b):
        nonlocal all_called
        all_called = True

        assert a == "foo"
        assert b == 42
        assert bot == frozenbot

        # It's not possible to check from the public API if the shared instance
        # is the right one
        assert shared is not None

    # One extra argument
    def more(bot, a, c):
        assert 2 + 2 == 5

    for func in subset, all:
        frozenbot._call(func, "comptest", a="foo", b=42)

    # More should raise a TypeError for the "c" argument
    with pytest.raises(TypeError):
        frozenbot._call(more, "comptest", a="foo", b=42)

    assert subset_called
    assert all_called


def test_available_commands(bot):
    # Create a bunch of dummy commands
    @bot.command("test1", order=10)
    def test1():
        pass

    @bot.command("test2")
    def test2():
        pass

    @bot.command("test3", hidden=True)
    def test3():
        pass

    assert [cmd.name for cmd in bot.available_commands()] == [
        "help",
        "test2",
        "test1",
    ]

    assert [cmd.name for cmd in bot.available_commands(all=True)] == [
        "help",
        "start",
        "test2",
        "test3",
        "test1",
    ]


def test_pickle_frozenbot(frozenbot):
    # This will pickle and unpickle the frozen bot
    pickled = pickle.loads(pickle.dumps(frozenbot))
    assert frozenbot == pickled
