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


def test_unavailable_chats(api, mock_req):
    # A bunch of mocked requests for the API
    mock_req({
        "sendMessage": {"ok": True, "result": {}},
        "forwardMessage": {
            "ok": False, "error_code": 123,
            "description": "This is a message!",
        },
        "sendPhoto": {
            "ok": False, "error_code": 403,
            "description": "This is not the message you want!",
        },
        "sendAudio": {
            "ok": False, "error_code": 123,
            "description": "Bot was blocked by the user",
        },
        "sendDocument": {
            "ok": False, "error_code": 403,
            "description": "Bot was blocked by the user",
        },
        "sendSticker": {
            "ok": False, "error_code": 400,
            "description": "Bad request: chat not found",
        },
        "sendVideo": {
            "ok": False, "error_code": 403,
            "description": "Forbidden: bot was kicked from the group chat",
        },
        "sendLocation": {
            "ok": False, "error_code": 400,
            "description": "Bad request: PEER_ID_INVALID",
        },
        "sendVoice": {
            "ok": False, "error_code": 403,
            "description": "Forbidden: user is deactivated",
        },
        "sendChatAction": {
            "ok": False, "error_code": 400,
            "description":
                "Bad Request: group chat is migrated to a supergroup chat",
        },
        "getMe": {
            "ok": False, "error_code": 403,
            "description": "Bot was blocked by the user",
        },
    })

    # Test a successiful request
    api.call("sendMessage", {"chat_id": 123})

    # Test a failed request with wrong error code and description
    with pytest.raises(botogram.api.APIError) as e:
        api.call("forwardMessage", {"chat_id": 123})
    assert e.type != botogram.api.ChatUnavailableError

    # Test a failed request with matching error code and wrong description
    with pytest.raises(botogram.api.APIError) as e:
        api.call("sendPhoto", {"chat_id": 123})
    assert e.type != botogram.api.ChatUnavailableError

    # Test a failed request with wrong error code and matching description
    with pytest.raises(botogram.api.APIError) as e:
        api.call("sendAudio", {"chat_id": 123})
    assert e.type != botogram.api.ChatUnavailableError

    # Test a failed request with matching error code and description for
    # blocked users
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("sendDocument", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "blocked"

    # Test a failed request with matching error code and description for chats
    # not found
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("sendSticker", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "not_found"

    # Test a failed request with matching error code and description for a bot
    # kicked from the group
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("sendVideo", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "kicked"

    # Test a failed request with matching error code and description, and in
    # which Telegram failed to determine the reason why the user can't be
    # contacted
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("sendLocation", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "not_found"

    # Test a failed request with matching error code and description to an user
    # which deleted its account
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("sendVoice", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "account_deleted"

    # Test a failed request with right error code and descriptio to the wrong
    # method (not a method which sends things to users)
    with pytest.raises(botogram.api.APIError) as e:
        api.call("getMe", {"chat_id": 123})
    assert e.type != botogram.api.ChatUnavailableError


def test_unavailable_chats_take2(api, mock_req):
    # I just finished the list of methods I can mock in the previous test, lol
    # A bunch of mocked requests for the API
    mock_req({
        "sendMessage": {"ok": True, "result": {}},
        "forwardMessage": {
            "ok": False, "error_code": 400,
            "description":
                "Bad Request: group chat is migrated to a supergroup chat",
        },
    })

    # Test a failed request with matching error code and description to a group
    # chat which was converted to a supergroup
    with pytest.raises(botogram.api.ChatUnavailableError) as e:
        api.call("forwardMessage", {"chat_id": 123})
    assert e.value.chat_id == 123
    assert e.value.reason == "chat_moved"
