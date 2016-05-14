"""
    Tests for botogram/frozenbot.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

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
    @bot.command("test1")
    def test1():
        pass

    @bot.command("test2")
    def test2():
        pass

    @bot.command("test3", hidden=True)
    def test3():
        pass

    assert {cmd.name for cmd in bot.available_commands()} == {
        "help",
        "test1",
        "test2",
    }

    assert {cmd.name for cmd in bot.available_commands(all=True)} == {
        "help",
        "start",
        "test1",
        "test2",
        "test3",
    }


def test_pickle_frozenbot(frozenbot):
    # This will pickle and unpickle the frozen bot
    pickled = pickle.loads(pickle.dumps(frozenbot))
    assert frozenbot == pickled
