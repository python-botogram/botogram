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

import re

from .callbacks import hashed_callback_name
from .context import Context


class Hook:
    """Base class for all the hooks"""

    _only_texts = False
    _botogram_hook = True

    def __init__(self, func, component, args=None):
        prefix = ""
        if component.component_name:
            prefix = component.component_name + "::"

        self.func = func
        self.name = prefix + func.__name__
        self.component = component
        self.component_id = component._component_id

        self._args = args
        self._after_init(args)

    def __reduce__(self):
        return rebuild, (self.__class__, self.func, self.component, self._args)

    def __repr__(self):
        return "<" + self.__class__.__name__ + " \"" + self.name + "\">"

    def _after_init(self, args):
        """Prepare the object"""
        pass

    def call(self, bot, update):
        """Call the hook"""
        with Context(bot, self, update):
            if self._only_texts and update.message.text is None:
                return
            return self._call(bot, update)

    def _call(self, bot, update):
        """*Actually* call the hook"""
        message = update.message
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


def rebuild(cls, func, component, args):
    hook = cls(func, component, args)
    return hook


class BeforeProcessingHook(Hook):
    """Underlying hook for @bot.process_message"""
    pass


class ProcessMessageHook(Hook):
    """Underlying hook for @bot.process_message"""
    pass


class MemoryPreparerHook(Hook):
    """Underlying hook for @bot.prepare_memory"""

    def call(self, memory):
        return self.func(memory)


class NoCommandsHook(Hook):
    """Underlying hook for an internal event"""
    pass


class MessageEqualsHook(Hook):
    """Underlying hook for @bot.message_equals"""

    _only_texts = True

    def _after_init(self, args):
        if args["ignore_case"]:
            self._string = args["string"].lower()
        else:
            self._string = args["string"]

    def _prepare(self, update):
        message = update.message
        text = message.text
        if self._args["ignore_case"]:
            text = text.lower()

        return message, text

    def _call(self, bot, update):
        message, text = self._prepare(update)

        if text != self._string:
            return
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


class MessageContainsHook(MessageEqualsHook):
    """Underlying hook for @bot.message_contains"""

    _only_texts = True

    def _call(self, bot, update):
        message, text = self._prepare(update)
        splitted = text.split(" ")

        res = []
        for one in splitted:
            if one != self._string:
                continue

            result = bot._call(self.func, self.component_id, chat=message.chat,
                               message=message)
            res.append(result)
            if not self._args["multiple"]:
                break

        return len(res) > 0


class MessageMatchesHook(Hook):
    """Underlying hook for @bot.message_matches"""

    _only_texts = True

    def _after_init(self, args):
        self._regex = re.compile(args["regex"], flags=args["flags"])

    def _call(self, bot, update):
        message = update.message
        results = self._regex.finditer(message.text)

        found = False
        for result in results:
            found = True

            bot._call(self.func, self.component_id, chat=message.chat,
                      message=message, matches=result.groups())
            if not self._args["multiple"]:
                break

        return found


_command_args_split_re = re.compile(r' +')


class CommandHook(Hook):
    """Underlying hook for @bot.command"""

    _only_texts = True

    def _after_init(self, args):
        # Check if the command name is valid
        if not re.match(r'^[a-zA-Z0-9_]+$', args["name"]):
            raise ValueError("Invalid command name: %s" % args["name"])

        # This regex will match all commands pointed to this bot
        self._regex = re.compile(r'^\/' + args["name"] + r'(@[a-zA-Z0-9_]+)?'
                                 r'( .*)?$')

        self._name = args["name"]
        self._hidden = False
        if "hidden" in args:
            self._hidden = args["hidden"]
        self._order = 0
        if "order" in args:
            self._order = args["order"]

    def _call(self, bot, update):
        message = update.message
        text = message.text.replace("\n", " ").replace("\t", " ")

        # Must be the correct command for the correct bot
        match = self._regex.match(text)
        if not match:
            return
        if match.group(1) and match.group(1) != "@" + bot.itself.username:
            return

        args = _command_args_split_re.split(text)[1:]
        bot._call(self.func, self.component_id, chat=message.chat,
                  message=message, args=args)
        return True


class CallbackHook(Hook):
    """Underlying hook for @bot.callback"""

    def _after_init(self, args):
        self._name = hashed_callback_name(
            "%s:%s" % (self.component.component_name, args["name"])
        )

    def call(self, bot, update, name, data):
        with Context(bot, self, update):
            if not update.callback_query:
                return
            q = update.callback_query

            if name != self._name:
                return

            bot._call(
                self.func, self.component_id, query=q, chat=q.message.chat,
                message=q.message, data=data,
            )

            update.callback_query._maybe_send_noop()
            return True


class ChatUnavailableHook(Hook):
    """Underlying hook for @bot.chat_unavailable"""

    def call(self, bot, chat_id, reason):
        with Context(bot, self, None):
            return bot._call(self.func, self.component_id, chat_id=chat_id,
                             reason=reason)


class MessageEditedHook(Hook):
    """Underlying hook for @bot.message_edited"""

    def _call(self, bot, update):
        message = update.edited_message
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


class ChannelPostHook(Hook):
    """Underlying hook for @bot.channel_post"""

    def _call(self, bot, update):
        message = update.channel_post
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


class EditedChannelPostHook(Hook):
    """Underlying hook for @bot.channel_post_edited"""

    def _call(self, bot, update):
        message = update.edited_channel_post
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


class TimerHook(Hook):
    """Underlying hook for a timer"""

    def call(self, bot):
        with Context(bot, self, None):
            return bot._call(self.func, self.component_id)
