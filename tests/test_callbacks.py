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

import json

import pytest

from botogram.callbacks import Buttons, parse_callback_data, get_callback_data
from botogram.callbacks import hashed_callback_name
from botogram.components import Component
from botogram.context import Context
from botogram.crypto import TamperedMessageError
from botogram.hooks import Hook


def test_buttons(bot, sample_update):
    component = Component("test")
    hook = Hook(lambda: None, component)

    buttons = Buttons()
    buttons[0].url("test 1", "http://example.com")
    buttons[0].callback("test 2", "test_callback")
    buttons[3].callback("test 3", "another_callback", "data")
    buttons[2].switch_inline_query("test 4")
    buttons[2].switch_inline_query("test 5", "wow", current_chat=True)

    with Context(bot, hook, sample_update):
        assert buttons._serialize_attachment(sample_update.chat()) == {
            "inline_keyboard": [
                [
                    {"text": "test 1", "url": "http://example.com"},
                    {
                        "text": "test 2",
                        "callback_data": get_callback_data(
                            bot, sample_update.chat(), "test:test_callback",
                        ),
                    },
                ],
                [
                    {"text": "test 4", "switch_inline_query": ""},
                    {
                        "text": "test 5",
                        "switch_inline_query_current_chat": "wow"
                    },
                ],
                [
                    {
                        "text": "test 3",
                        "callback_data": get_callback_data(
                            bot, sample_update.chat(), "test:another_callback",
                            "data",
                        ),
                    },
                ],
            ],
        }


def test_parse_callback_data(bot, sample_update):
    c = sample_update.chat()

    raw = get_callback_data(bot, c, "test_callback", "this is some data!")
    assert parse_callback_data(bot, c, raw) == (
        hashed_callback_name("test_callback"),
        "this is some data!",
    )

    raw = get_callback_data(bot, c, "test_callback")
    assert parse_callback_data(bot, c, raw) == (
        hashed_callback_name("test_callback"),
        None,
    )

    with pytest.raises(TamperedMessageError):
        raw = get_callback_data(bot, c, "test_callback", "data") + "!"
        parse_callback_data(bot, c, raw)

    # Now test with disabled signature verification
    bot.validate_callback_signatures = False

    raw = get_callback_data(bot, c, "test_callback", "data") + "!"
    assert parse_callback_data(bot, c, raw) == (
        hashed_callback_name("test_callback"),
        "data!"
    )
