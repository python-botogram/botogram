"""
    botogram.api
    Wrapper for the Telegram Bot API

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import requests

from . import exceptions as exc


# These API methods sends something to a chat
# This list is used to filter which method to check for unavailable chats
SEND_TO_CHAT_METHODS = (
    "sendMessage",
    "forwardMessage",
    "sendPhoto",
    "sendAudio",
    "sendDocument",
    "sendSticker",
    "sendVideo",
    "sendVoice",
    "sendLocation",
    "sendChatAction",
)


class TelegramAPI:
    """Main interface to the Telegram API"""

    def __init__(self, api_key, endpoint=None):
        # Fill the default API endpoint
        if endpoint is None:
            endpoint = "https://api.telegram.org/"

        self._api_key = api_key
        self._endpoint = endpoint

    def call(self, method, params=None, files=None, expect=None):
        """Call a method of the API"""
        url = self._endpoint + "bot%s/%s" % (self._api_key, method)
        response = requests.get(url, params=params, files=files)
        content = response.json()

        if not content["ok"]:
            status = content["error_code"]
            message = content["description"]

            # Special handling for unavailable chats
            if method in SEND_TO_CHAT_METHODS:
                reason = None
                if status == 403 and "blocked" in message:
                    reason = "blocked"
                elif status == 403 and "deleted user" in message:
                    reason = "account_deleted"
                elif status == 400 and "PEER_ID_INVALID" in message:
                    # What, this error is an identifier and not a sentence :/
                    reason = "not_contacted"
                elif status == 400 and "not found" in message:
                    reason = "not_found"
                elif status == 403 and "kicked" in message:
                    reason = "kicked"
                elif status == 400 and "deactivated" in message:
                    reason = "chat_moved"

                if reason is not None:
                    raise exc.ChatUnavailableError(reason, params["chat_id"])

            raise exc.APIError(content)

        # If no special object is expected, return the decoded json.
        # Else, return the "pythonized" result
        if expect is None:
            return content
        else:
            wrapped = expect(content["result"])
            if hasattr(wrapped, "set_api"):
                wrapped.set_api(self)
            return wrapped

    def file_content(self, path):
        """Get the content of an user-submitted file"""
        url = self._endpoint + "file/bot%s/%s" % (self._api_key, path)
        response = requests.get(url)

        return response.content
