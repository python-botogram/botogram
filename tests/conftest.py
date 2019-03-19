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
                "type": "group",
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
