"""
    Tests for botogram/bot.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import copy

import botogram.bot
import botogram.components

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
