"""
    botogram.exceptions
    A collection of all the exceptions raised by botogram

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


class BotogramError(Exception):
    """The parent of all the errors raised by botogram"""

    def __init__(self, msg):
        self.msg = msg


class APIError(BotogramError):
    """Something went wrong with the upstream Telegram API"""

    def __init__(self, response):
        self.error_code = response["error_code"]
        self.description = response["description"]

        self.msg = "Request failed with code %s. Response from Telegram: " \
            "\"%s\"" % (self.error_code, self.description)


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

        self.msg = msg


class FetchError(APIError):
    """Something went wrong while fetching updates"""

    def __init__(self, msg):
        self.msg = msg


class AnotherInstanceRunningError(FetchError):
    """Another instance of your bot is running somewhere else"""

    def __init__(self):
        self.msg = "Request terminated because of another long pooling or " \
                   "webhook active"
