"""
    botogram.objects.updates
    Representation of updates-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .base import BaseObject, multiple

from .messages import Message
from .payments import ShippingQuery, PreCheckoutQuery


class Update(BaseObject):
    """Telegram API representation of an update

    https://core.telegram.org/bots/api#update
    """

    required = {
        "update_id": int,
    }
    optional = {
        "message": Message,
        "edited_message": Message,
        "channel_post": Message,
        "edited_channel_post": Message,
        "shipping_query": ShippingQuery,
        "pre_checkout_query": PreCheckoutQuery,
    }
    _check_equality_ = "update_id"


# Shortcut for the Updates type
Updates = multiple(Update)
