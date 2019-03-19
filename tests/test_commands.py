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

import botogram.commands
import botogram.decorators


BAD_DOCSTRING = """ a


  b

"""


def global_command():
    pass


def create_command(bot, name, func=None):
    """Create a new command"""
    if func is None:
        def func():
            pass

    bot.command(name)(func)

    all_commands = {cmd.name: cmd for cmd in bot.available_commands(True)}
    return func, all_commands[name]


def test_command_pickling(bot):
    # First of all create a dummy Command
    func, cmd = create_command(bot, "test", func=global_command)

    assert cmd.name == pickle.loads(pickle.dumps(cmd)).name


def test_command_for_bot(bot):
    # First of all create a dummy Command and an instance of it without a bot
    func, cmd1 = create_command(bot, "test")
    cmd2 = cmd1.for_bot(None)  # Strip away the bot

    assert cmd1._bot == bot
    assert cmd2._bot == None
    assert cmd1 is not cmd2


def test_command_raw_docstring(bot):
    global_bot = bot

    # First of all create a command
    func, cmd = create_command(bot, "test")

    # With no docstring
    assert cmd.raw_docstring is None

    # With a basic docstring
    func.__doc__ = "test1"
    assert cmd.raw_docstring == "test1"

    # With a custom help message
    @botogram.decorators.help_message_for(func)
    def test2(bot):
        # Check if arguments are provided correctly
        assert bot == global_bot

        return "test2"

    assert cmd.raw_docstring == "test2"

    # With a custom help message but without a bot
    cmd = cmd.for_bot(None)

    @botogram.decorators.help_message_for(func)
    def test3():
        return "test3"

    assert cmd.raw_docstring == "test3"


def test_command_docstring(bot):
    # First of all create a command
    func, cmd = create_command(bot, "test")

    # A docstring which contains every bad thing
    func.__doc__ = BAD_DOCSTRING
    assert cmd.docstring == "a\n\nb"

    # A simple but correct docstring
    func.__doc__ = "a\nb"
    assert cmd.docstring == "a\nb"


def test_command_summary(bot):
    # First of all create a command
    func, cmd = create_command(bot, "test")

    # Summary of a docstring with only one line
    func.__doc__ = "This is a test"
    assert cmd.summary == "This is a test"

    # Summary of a docstring with more than one lines
    func.__doc__ = "This is a\nlong test"
    assert cmd.summary == "This is a"
