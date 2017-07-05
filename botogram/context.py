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

import threading


_local = threading.local()
_local._botogram_context = []


class Context:
    """Context of an hook call"""

    def __init__(self, bot, hook, update):
        self.bot = bot
        self.hook = hook
        self.update = update

    def __enter__(self):
        _local._botogram_context.append(self)

    def __exit__(self, *_):
        _local._botogram_context.pop()

    def bot_username(self):
        """Get the username of the bot"""
        return self.bot.itself.username

    def component_name(self):
        """Get the name of the current component"""
        return self.hook.component.component_name

    def chat(self):
        """Get the current chat"""
        if self.update:
            return self.update.chat()


def ctx():
    """Get the current context"""
    if _local._botogram_context:
        return _local._botogram_context[-1]
