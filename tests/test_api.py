"""
    Tests for botogram/api.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.api
import botogram.objects


def test_api_call(api, mock_req):
    # This will mock the requests the API will made
    mock_req({
        "getMe": {"ok": True, "result": {"id": 1, "first_name": "test"}},
        "wrong": {"ok": False, "error_code": 123, "description": "test"},
    })

    # First try to get the raw result
    result = api.call("getMe")
    assert result == {"ok": True, "result": {"id": 1, "first_name": "test"}}

    # Next try to wrap it in an object
    result = api.call("getMe", expect=botogram.objects.User)
    assert result.id == 1
    assert result.first_name == "test"
    assert isinstance(result, botogram.objects.User)

    # And then try to call something which doesn't exist
    with pytest.raises(botogram.api.APIError):
        result = api.call("wrong")
