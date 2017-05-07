"""
    botogram.objects.callback_query
    Representation of the callback query-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .base import BaseObject

from .messages import User, Message


class CallbackQuery(BaseObject):
    """Telegram API representation of a callback query

    https://core.telegram.org/bots/api#callbackquery
    """

    required = {
        "id": str,
        "from": User,
        "message": Message,
        "chat_instance": str,
    }
    optional = {
        "inline_message_id": str,
        "data": str,
        "game_short_name": str,
    }
    replace_keys = {
        "from": "sender",
    }
