"""
    botogram.hooks
    Logic for all the hooks

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re


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


class ChatUnavailableHook(Hook):
    """Underlying hook for @bot.chat_unavailable"""

    def call(self, bot, chat_id, reason):
        return bot._call(self.func, self.component_id, chat_id=chat_id,
                         reason=reason)


class MessageEditedHook(Hook):
    """Underlying hook for @bot.message_edited"""

    def _call(self, bot, update):
        message = update.edited_message
        return bot._call(self.func, self.component_id, chat=message.chat,
                         message=message)


class TimerHook(Hook):
    """Underlying hook for a timer"""

    def call(self, bot):
        return bot._call(self.func, self.component_id)
