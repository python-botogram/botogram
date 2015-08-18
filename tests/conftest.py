"""
    Configuration file for tests

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import json

import pytest
import responses

import botogram.api


API_KEY = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"


@pytest.fixture()
def mock_req(request):
    """Shortcut for mocking a request"""
    responses.start()
    request.addfinalizer(lambda: responses.stop())

    def __(method, response):
        responses.add("GET", "https://api.telegram.org/bot"+API_KEY+"/"+method,
                      content_type="application/json",
                      body=json.dumps(response))

    return __


@pytest.fixture()
def api(request):
    return botogram.api.TelegramAPI(API_KEY)
