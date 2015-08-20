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
    @bot.process_message
    @botogram.utils.pass_bot
    def process_message(local_bot, chat, message):
        assert local_bot is bot

    bot.process(sample_update)
