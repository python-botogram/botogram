"""
    Tests for botogram/utils.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import botogram.decorators


def test_help_message_for(bot):

    @bot.command("test")
    def func():
        """docstring"""
        pass

    cmd = {cmd.name: cmd for cmd in bot.available_commands()}["test"]

    assert cmd.raw_docstring == "docstring"

    @botogram.decorators.help_message_for(func)
    def help_func():
        return "function"

    assert cmd.raw_docstring == "function"
