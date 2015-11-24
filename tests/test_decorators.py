"""
    Tests for botogram/utils.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import botogram.decorators
import botogram.utils


def test_help_message_for():

    def func():
        """docstring"""
        pass

    assert botogram.utils.docstring_of(func) == "docstring"

    @botogram.decorators.help_message_for(func)
    def help_func():
        return "function"

    assert botogram.utils.docstring_of(func) == "function"
