"""
    botogram.api
    Wrapper for the Telegram Bot API

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import requests


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
    "getChat",
)


class APIError(Exception):
    """Something went wrong with the API"""

    def __init__(self, response):
        self.error_code = response["error_code"]
        self.description = response["description"]

        msg = "Request failed with code %s. Response from Telegram: \"%s\"" % (
            self.error_code, self.description
        )

        super(APIError, self).__init__(msg)


class ChatUnavailableError(APIError):
    """A chat is unavailable, which means you can't send messages to it"""

    def __init__(self, reason, chat_id):
        self.reason = reason
        self.chat_id = chat_id

        if reason == "blocked":
            msg = "The user with ID %s blocked your bot" % chat_id
        elif reason == "account_deleted":
            msg = "The user with ID %s deleted his account" % chat_id
        elif reason == "not_contacted":
            msg = "The user with ID %s didn't contact you before" % chat_id
        elif reason == "not_found":
            msg = "The chat with ID %s doesn't exist" % chat_id
        elif reason == "kicked":
            msg = "The bot was kicked from the group with ID %s" % chat_id
        elif reason == "chat_moved":
            msg = "The chat with ID %s moved, and the old ID is no longer " \
                  "valid" % chat_id
        else:
            raise ValueError("Unknown reason: %s" % reason)

        Exception.__init__(self, msg)


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

                # This happens when the bot tries to send messages to an user
                # who blocked the bot
                if status == 403 and "blocked" in message:
                    # Error code # 403
                    # Bot was blocked by the user
                    reason = "blocked"

                # This happens when the user deleted its account
                elif status == 403 and "deleted" in message:
                    # Error code # 403
                    # Forbidden: user is deleted
                    reason = "account_deleted"

                # This happens, as @BotSupport says, when the Telegram API
                # isn't able to determine why your bot can't contact an user
                elif status == 400 and "PEER_ID_INVALID" in message:
                    # Error code # 400
                    # Bad request: PEER_ID_INVALID
                    reason = "not_found"

                # This happens when the bot can't contact the user or the user
                # doesn't exist
                elif status == 400 and "not found" in message:
                    # Error code # 400
                    # Bad Request: chat not found
                    reason = "not_found"

                # This happens when the bot is kicked from the group chat it's
                # trying to send messages to
                elif status == 403 and "kicked" in message:
                    # Error code # 403
                    # Forbidden: bot was kicked from the group chat
                    # Forbidden: bot was kicked from the supergroup chat
                    reason = "kicked"

                # This happens when the ID points to a group chat, which was
                # migrated to a supergroup chat, thus changing its ID
                elif status == 400 and "migrated" in message:
                    # Error code # 400
                    # Bad Request: group chat is migrated to a supergroup chat
                    reason = "chat_moved"

                if reason is not None:
                    raise ChatUnavailableError(reason, params["chat_id"])

            raise APIError(content)

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
