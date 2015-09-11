"""
    Configuration file for tests

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import json

import pytest
import responses

import botogram.api
import botogram.bot
import botogram.objects


API_KEY = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"


@pytest.fixture()
def mock_req(request):
    """Shortcut for mocking a request"""
    def __(requests):
        mocker = responses.RequestsMock(assert_all_requests_are_fired=False)
        mocker.start()

        request.addfinalizer(lambda: mocker.stop())

        for method, response in requests.items():
            mocker.add("GET",
                       "https://api.telegram.org/bot"+API_KEY+"/"+method,
                       content_type="application/json",
                       body=json.dumps(response))

    return __


@pytest.fixture()
def api(request):
    return botogram.api.TelegramAPI(API_KEY)


@pytest.fixture()
def bot(request):
    mocker = responses.RequestsMock()
    mocker.add("GET", "https://api.telegram.org/bot"+API_KEY+"/getMe",
               content_type="application/json", body=json.dumps({
                   "ok": True, "result": {"id": 1, "first_name": "test",
                   "username": "test_bot"}}))

    with mocker:
        bot = botogram.bot.create(API_KEY)
    return bot


@pytest.fixture()
def frozenbot(bot):
    return bot.freeze()


@pytest.fixture()
def sample_update(request):
    return botogram.objects.Update({
        "update_id": 1,
        "message": {
            "message_id": 2,
            "chat": {
                "id": -1,
                "title": "test",
            },
            "from": {
                "id": 3,
                "first_name": "test",
            },
            "date": 4,
            "text": "test",
        },
    })
