"""
    botogram.objects.callback_query
    Representation of the callback query-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .base import BaseObject

from .messages import User, Message
from . import mixins


class CallbackQuery(BaseObject, mixins.CallbackMixin):
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

    def __init__(self, data, api=None):
        super().__init__(data, api)
