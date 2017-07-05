# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
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

from .base import BaseObject
from ..context import ctx
from .messages import User, Message
from .mixins import _require_api


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
        "data": "_data",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._answered = False

    @_require_api
    def notify(self, text, alert=False, cache=0):
        """Send a notification or an alert to the user"""
        self._answered = True

        self._api.call("answerCallbackQuery", {
            "callback_query_id": self.id,
            "text": text,
            "show_alert": alert,
            "cache_time": cache,
        })

    @_require_api
    def open_url(self, url, cache=0):
        """Tell the user's client to open an URL"""
        self._answered = True

        self._api.call("answerCallbackQuery", {
            "callback_query_id": self.id,
            "url": url,
            "cache_time": cache,
        })

    @_require_api
    def open_private_chat(self, start_arg, cache=0):
        """Open the bot private chat with the user"""
        self._answered = True

        # Telegram doesn't support opening private chats with empty parameters,
        # so here we present the developer a friendlier message
        if not start_arg:
            raise ValueError("You must provide a non-empty start argument")

        # Construct the correct link
        url = "https://t.me/" + ctx().bot_username() + "?start=" + start_arg

        self._api.call("answerCallbackQuery", {
            "callback_query_id": self.id,
            "url": url,
            "cache_time": cache,
        })

    @_require_api
    def _maybe_send_noop(self):
        """Internal function to hide the spinner if needed"""
        if self._answered:
            return

        # Only call this if the query wasn't answered before
        self._api.call("answerCallbackQuery", {
            "callback_query_id": self.id,
            "cache_time": 0
        })
