"""
    botogram.objects.mixins
    Additional management methods for upstream API objects

    Copyright (c) 2015 Pietro Albini
    Released under the MIT license
"""

import functools


def _require_api(func):
    """Decorator which forces to have the api on an object"""
    @functools.wraps(func)
    def __(self, *args, **kwargs):
        if not hasattr(self, "_api") or self._api is None:
            raise RuntimeError("An API instance must be provided")
        return func(*args, **kwargs)
    return __


class ChatMixin:
    """Add some methods for chats"""

    @_require_api
    def send(self, message, preview=True, reply_to=None, extra=None):
        """Send a message"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Build API call arguments
        args = {"chat_id": self.id, "text": message,
                "disable_web_page_preview": not preview}
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        return self._api.call("sendMessage", args, Message)
