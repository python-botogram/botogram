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

import copy

import botogram.bot
import botogram.components
import botogram.utils

import conftest


def test_bot_creation(api, mock_req):
    # Mock the getMe request
    mock_req({
        "getMe": {"ok": True, "result": {"id": 1, "first_name": "test",
                                         "username": "test_bot"}},
    })

    bot1 = botogram.bot.create(conftest.API_KEY)
    bot2 = botogram.bot.Bot(api)
    for bot in bot1, bot2:
        assert bot.itself.id == 1
        assert bot.itself.first_name == "test"


def test_use_components(bot, sample_update):
    comp1 = botogram.components.Component()
    comp2 = botogram.components.Component()

    hook1_called = False
    hook2_called = False

    def hook1(chat, message):
        nonlocal hook1_called
        hook1_called = True

    def hook2(chat, message):
        nonlocal hook2_called
        hook2_called = True

        # This should be executed before hook_1
        assert not hook1_called

    comp1.add_process_message_hook(hook1)
    comp2.add_process_message_hook(hook2)

    # comp2 is registered after comp1, so their hooks should be called before
    # the comp1's ones
    bot.use(comp1)
    bot.use(comp2)
    bot.process(sample_update)

    assert hook1_called
    assert hook2_called


def test_bot_freeze(bot):
    # Create the frozen bot instance
    frozen = bot.freeze()

    assert bot == frozen


def test_i18n_override(bot):
    default_message = botogram.utils.get_language("en") \
        .gettext("Use /help to get a list of all the commands.")
    override_message = "git gud"

    bot.override_i18n = {
        default_message: override_message
    }

    assert bot._("Use /help to get a list of all the commands.") \
        == override_message

    bot.override_i18n = {}

    assert bot._("Use /help to get a list of all the commands.") \
        == default_message
