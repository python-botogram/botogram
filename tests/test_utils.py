"""
    Tests for botogram/utils.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import botogram.utils


STRANGE_DOCSTRING = """ a


  b

"""


def test_format_docstr():
    # This docstring needs lots of cleanup...
    res = botogram.utils.format_docstr(STRANGE_DOCSTRING)
    assert res == "a\n\nb"

    # This instead should be left as it is
    ok = "a\nb"
    assert botogram.utils.format_docstr(ok) == ok


def test_pass_bot(bot, sample_update):
    @botogram.utils.pass_bot
    def func(local_bot, *args, **kwargs):
        assert local_bot is bot

    decorators = [
        bot.before_processing,
        bot.process_message,
        bot.message_contains("test1"),
        bot.message_matches(r"^test2$"),
        bot.command("test3")
    ]

    for decorator in decorators:
        func = decorator(func)

    for msg in "test1", "test2", "/test3":
        sample_update.message.text = msg
        bot.process(sample_update)
