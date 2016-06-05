"""
    Tests for botogram/api.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.api
import botogram.exceptions
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
    with pytest.raises(botogram.exceptions.APIError):
        result = api.call("wrong")


def test_unavailable_chats(api, mock_req):
    # A bunch of mocked requests for the API
    mock_req({
        "sendMessage": {"ok": True, "result": {}},
        "forwardMessage": {
            "ok": False, "error_code": 123, "description": "test",
        },
        "sendPhoto": {
            "ok": False, "error_code": 403, "description": "test",
        },
        "sendAudio": {
            "ok": False, "error_code": 123, "description": "blocked test",
        },
        "sendDocument": {
            "ok": False, "error_code": 403, "description": "blocked test",
        },
        "sendSticker": {
            "ok": False, "error_code": 400, "description": "chat not found",
        },
        "sendVideo": {
            "ok": False, "error_code": 403, "description": "I was kicked!",
        },
        "sendLocation": {
            "ok": False, "error_code": 400, "description": "PEER_ID_INVALID",
        },
        "sendVoice": {
            "ok": False, "error_code": 403, "description": "a deleted user",
        },
        "getMe": {
            "ok": False, "error_code": 403, "description": "blocked test",
        },
    })

    # Test a successiful request
    api.call("sendMessage", {"chat_id": 123})

    # Test a failed request with wrong error code and description
    with pytest.raises(botogram.exceptions.APIError) as e:
        api.call("forwardMessage", {"chat_id": 123})
    assert e.type != botogram.exceptions.ChatUnavailableError

    # Test a failed request with matching error code and wrong description
    with pytest.raises(botogram.exceptions.APIError) as e:
        api.call("sendPhoto", {"chat_id": 123})
    assert e.type != botogram.exceptions.ChatUnavailableError

    # Test a failed request with wrong error code and matching description
    with pytest.raises(botogram.exceptions.APIError) as e:
        api.call("sendAudio", {"chat_id": 123})
    assert e.type != botogram.exceptions.ChatUnavailableError

    # Test a failed request with matching error code and description for
    # blocked users
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("sendDocument", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "blocked"

    # Test a failed request with matching error code and description for chats
    # not found
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("sendSticker", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "not_found"

    # Test a failed request with matching error code and description for a bot
    # kicked from the group
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("sendVideo", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "kicked"

    # Test a failed request with matching error code and description to an user
    # which hasn't contacted your bot yet
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("sendLocation", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "not_contacted"

    # Test a failed request with matching error code and description to an user
    # which deleted its account
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("sendVoice", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "account_deleted"

    # Test a failed request with right error code and descriptio to the wrong
    # method (not a method which sends things to users)
    with pytest.raises(botogram.exceptions.APIError) as e:
        api.call("getMe", {"chat_id": 123})
    assert e.type != botogram.exceptions.ChatUnavailableError


def test_unavailable_chats_take2(api, mock_req):
    # I just finished the list of methods I can mock in the previous test, lol
    # A bunch of mocked requests for the API
    mock_req({
        "sendMessage": {"ok": True, "result": {}},
        "forwardMessage": {
            "ok": False, "error_code": 400, "description": "chat deactivated",
        },
    })

    # Test a failed request with matching error code and description to a group
    # chat which was converted to a supergroup
    with pytest.raises(botogram.exceptions.ChatUnavailableError) as e:
        api.call("forwardMessage", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "chat_moved"
