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

from .base import BaseObject, multiple

from .callbacks import CallbackQuery
from .messages import Message


class Update(BaseObject):
    """Telegram API representation of an update

    https://core.telegram.org/bots/api#update
    """

    # Please update the chat method below when adding new types, thanks!

    required = {
        "update_id": int,
    }
    optional = {
        "message": Message,
        "edited_message": Message,
        "channel_post": Message,
        "edited_channel_post": Message,
        "callback_query": CallbackQuery,
    }
    _check_equality_ = "update_id"

    def chat(self):
        """Get the chat related to this update"""
        if self.message is not None:
            return self.message.chat

        if self.edited_message is not None:
            return self.edited_message.chat

        if self.channel_post is not None:
            return self.channel_post.chat

        if self.edited_channel_post is not None:
            return self.edited_channel_post.chat

        if self.callback_query is not None:
            return self.callback_query.message.chat

        raise NotImplementedError


# Shortcut for the Updates type
Updates = multiple(Update)
