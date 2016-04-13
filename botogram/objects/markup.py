"""
    botogram.objects.markup
    Representation of reply markup-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


from .base import BaseObject, multiple


class ReplyKeyboardMarkup(BaseObject):
    """Telegram API representation of a custom keyboard

    https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    required = {
        "keyboard": multiple(multiple(str)),
    }
    optional = {
        "resize_keyboard": bool,
        "one_time_keyboard": bool,
        "selective": bool,
    }


class ReplyKeyboardHide(BaseObject):
    """Telegram API special object which hides a custom keyboard

    https://core.telegram.org/bots/api#replykeyboardhide
    """

    required = {
        "hide_keyboard": bool,
    }
    optional = {
        "selective": bool,
    }


class ForceReply(BaseObject):
    """Telegram API special object which forces the user to reply to a message

    https://core.telegram.org/bots/api#forcereply
    """

    required = {
        "force_reply": bool,
    }
    optional = {
        "selective": bool,
    }
