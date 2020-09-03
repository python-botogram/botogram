# Copyright (c) 2015-2020 The Botogram Authors (see AUTHORS)
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
from .messages import User, Location
from . import mixins
from .messages import Message


class InlineQuery(BaseObject, mixins.InlineMixin):
    required = {
        "id": str,
        "from": User,
        "query": str,
    }
    optional = {
        "location": Location,
        "offset": str,
    }
    replace_keys = {
        "from": "sender"
    }

    def __init__(self, data):
        super().__init__(data)
        self._switch_pm_text = None
        self._switch_pm_parameter = None

    def switch_pm(self, text, parameter):
        """Helper to set the switch_pm_text and switch_pm_parameter"""
        self._switch_pm_text = text
        self._switch_pm_parameter = parameter


class InlineFeedback(BaseObject):
    required = {
        "result_id": str,
        "from": User,
        "query": str
    }
    optional = {
        "location": Location,
        "inline_message_id": str,
    }
    replace_keys = {
        "from": "sender",
        "inline_message_id": "message"
    }

    def __init__(self, data, api=None):
        super().__init__(data, api)
        self.message = Message({"inline_message_id": self.message}, api)
