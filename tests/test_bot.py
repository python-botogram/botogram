"""
    Tests for botogram/bot.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import copy

import botogram.bot

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


def test_before_processing(bot, sample_update):
    # This will be true if the before_processing hook was processed
    before_hook_processed = False
    process_hook_processed = False

    # Configure the test bot
    @bot.before_processing
    def before_processing(chat, message):
        nonlocal before_hook_processed
        before_hook_processed = True

        # Test provided arguments are OK
        assert chat.id == -1
        assert message.text == "test"
        assert message.chat == chat

    # This will test if the hook processing order is right
    @bot.process_message
    def process_message(*__):
        nonlocal process_hook_processed
        process_hook_processed = True

        # Should be called after before_processing
        assert before_hook_processed

    bot.process(sample_update)

    assert before_hook_processed
    assert process_hook_processed


def test_process_message(bot, sample_update):
    # This will be true if the process_message hook was processed
    process_hook_processed = False

    # Configure the test bot
    @bot.process_message
    def process_message(chat, message):
        nonlocal process_hook_processed
        process_hook_processed = True

        # Test provided arguments are OK
        assert chat.id == -1
        assert message.text == "test"
        assert message.chat == chat

    bot.process(sample_update)

    assert process_hook_processed


def test_pass_bot(bot, sample_update):
    @bot.process_message
    @botogram.bot.pass_bot
    def process_message(local_bot, chat, message):
        assert local_bot is bot

    bot.process(sample_update)
