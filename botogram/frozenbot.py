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

import logbook

from . import utils
from . import objects
from . import api as api_module


class FrozenBotError(Exception):
    pass


class FrozenBot:
    """A frozen version of botogram.Bot"""

    def __init__(self, api, about, owner, hide_commands, before_help,
                 after_help, link_preview_in_help,
                 validate_callback_signatures, process_backlog, lang, itself,
                 commands_re, commands, chains, scheduler, main_component_id,
                 bot_id, shared_memory, update_processors, override_i18n):
        # This attribute should be added with the default setattr, because is
        # needed by the custom setattr
        object.__setattr__(self, "_frozen", False)

        # Restore original content
        self.api = api
        self.about = about
        self.owner = owner
        self._hide_commands = hide_commands
        self.before_help = before_help
        self.after_help = after_help
        self.link_preview_in_help = link_preview_in_help
        self.validate_callback_signatures = validate_callback_signatures
        self.process_backlog = process_backlog
        self.lang = lang
        self._commands_re = commands_re
        self._main_component_id = main_component_id
        self._bot_id = bot_id
        self._shared_memory = shared_memory
        self._scheduler = scheduler
        self._chains = chains
        self._update_processors = update_processors
        self._commands = {name: command.for_bot(self)
                          for name, command in commands.items()}
        self.override_i18n = override_i18n

        # Setup the logger
        self.logger = logbook.Logger('botogram bot')

        # Get a fresh Gettext instance
        self._lang_inst = utils.get_language(lang)

        # Prepare the bot representation
        self.itself = itself
        self.itself.set_api(api)

        # No more changes allowed!
        self._frozen = True

    def __reduce__(self):
        args = (
            self.api, self.about, self.owner, self._hide_commands,
            self.before_help, self.after_help, self.link_preview_in_help,
            self.validate_callback_signatures, self.process_backlog, self.lang,
            self.itself, self._commands_re, self._commands, self._chains,
            self._scheduler, self._main_component_id, self._bot_id,
            self._shared_memory, self._update_processors, self.override_i18n,
        )
        return restore, args

    def __setattr__(self, name, value):
        # _frozen marks if the object is frozen or not
        # This is useful because the init method needs to alter the object, but
        # after that no one should
        if self._frozen:
            raise FrozenBotError("Can't alter a frozen bot")

        return object.__setattr__(self, name, value)

    def __eq__(self, other):
        return self._bot_id == other._bot_id

    # All those methods do nothing, since you aren't allowed to change the
    # hooks a bot has in a frozen instance
    # All of those will be overridden in the Bot class

    def before_processing(self, func):
        """Register a before processing hook"""
        raise FrozenBotError("Can't add hooks to a bot at runtime")

    def process_message(self, func):
        """Register a message processor hook"""
        raise FrozenBotError("Can't add hooks to a bot at runtime")

    def message_equals(self, string, ignore_case=True):
        """Add a message equals hook"""
        raise FrozenBotError("Can't add hooks to a bot at runtime")

    def message_contains(self, string, ignore_case=True, multiple=False):
        """Add a message contains hook"""
        raise FrozenBotError("Can't add hooks to a bot at runtime")

    def message_matches(self, regex, flags=0, multiple=False):
        """Add a message matches hook"""
        raise FrozenBotError("Can't add hooks to a bot at runtime")

    def command(self, name, hidden=False):
        """Register a new command"""
        raise FrozenBotError("Can't add commands to a bot at runtime")

    def callback(self, name, hidden=False):
        """Register a new callback"""
        raise FrozenBotError("Can't add callbacks to a bot at runtime")

    def timer(self, interval):
        """Register a new timer"""
        raise FrozenBotError("Can't add timers to a bot at runtime")

    def prepare_memory(self, func):
        """Add a shared memory preparer"""
        raise FrozenBotError("Can't register a shared memory preparer to a "
                             "bot at runtime")

    @utils.deprecated("@bot.init_shared_memory", "1.0", "Rename the decorator "
                      "to @bot.prepare_memory")
    def init_shared_memory(self, func):
        """This decorator is deprecated, and it calls @prepare_memory"""
        return self.prepare_memory(func)

    # This class also contains methods to send messages to users
    # They're defined dynamically out of the class body, see below

    # Get a chat from its ID

    def chat(self, id):
        """Get an instance of botogram.Chat based on its ID"""
        return self.api.call("getChat", {"chat_id": id}, expect=objects.Chat)

    # Edit messages already sent

    def _edit_create_fake_message_object(self, chat, message):
        """Helper method for edit_message and edit_caption"""
        # Also accept objects
        if hasattr(message, "message_id"):
            message = message.message_id
        if hasattr(chat, "id"):
            chat = chat.id

        return objects.Message({
            "message_id": message,
            "from": {
                "id": self.itself.id,
                "first_name": "",
            },
            "date": 0,
            "chat": {
                "id": chat,
                "type": "",
            },
        }, self.api)

    def edit_message(self, chat, message, text, syntax=None, preview=True,
                     extra=None):
        """Edit a message already sent to the user"""
        msg = self._edit_create_fake_message_object(chat, message)
        msg.edit(text, syntax, preview, extra)

    def edit_caption(self, chat, message, caption, extra=None):
        """Edit the caption of a media already sent to the user"""
        msg = self._edit_create_fake_message_object(chat, message)
        msg.edit_caption(caption, extra)

    # Let's process the messages

    def process(self, update):
        """Process an update object"""
        if not isinstance(update, objects.Update):
            raise ValueError("Only Update objects are allowed")

        update.set_api(self.api)  # Be sure to use the correct API object

        try:
            for kind, processor in self._update_processors.items():
                # Call the processor of the right kind
                if getattr(update, kind) is None:
                    continue

                processor(self, self._chains, update)
                break
        except api_module.ChatUnavailableError as e:
            # Do some sane logging
            self.logger.warning("Chat %s is not available to your bot:" %
                                e.chat_id)
            self.logger.warning(str(e))
            self.logger.warning("Update #%s processing aborted!" %
                                update.update_id)

            for hook in self._chains["chat_unavalable_hooks"]:
                self.logger.debug("Executing %s for chat %s..." % (hook.name,
                                  e.chat_id))
                hook.call(self, e.chat_id, e.reason)

    def scheduled_tasks(self, current_time=None, wrap=True):
        """Return a list of tasks scheduled for now"""
        # This provides a better API for the users of the method
        def wrapper(task):
            def process():
                return task.process(self)
            return process

        # All the tasks returned are wrapped if wrap is True
        tasks = self._scheduler.now(current=current_time)
        if wrap:
            return [wrapper(job) for job in tasks]
        return list(tasks)

    def register_update_processor(self, kind, processor):
        """Register a new update processor"""
        raise FrozenBotError("Can't register new update processors at runtime")

    # This helper manages the translation

    def _(self, message, **args):
        """Translate a string"""
        # Check if the message has been overridden
        if message in self.override_i18n:
            return self.override_i18n[message] % args
        # Otherwise try to return the original message
        else:
            return self._lang_inst.gettext(message) % args

    # And some internal methods used by botogram

    def available_commands(self, all=False):
        """Get a list of the commands this bot implements"""
        s = sorted(self._commands.values(), key=lambda command: command.name)
        c = sorted(s, key=lambda command: command.order)

        for command in c:
            # Remove `or command.name in self.hide_commands` in botogram 1.0
            is_hidden = command.hidden or command.name in self._hide_commands
            if all or not is_hidden:
                yield command

    def _call(self, func, component=None, **available):
        """Wrapper for calling user-provided functions"""
        # Set some default available arguments
        available.setdefault("bot", self)

        # Add the `shared` argument only if a component was provided
        if component is not None:
            # It's lazily loaded so it won't make an IPC call on the runner
            def lazy_shared():
                return self._shared_memory.of(self._bot_id, component)

            available.setdefault("shared", utils.CallLazyArgument(lazy_shared))

        return utils.call(func, **available)

    # This function allows to use the old, deprecated bot.hide_commands

    @utils.deprecated("bot.hide_commands", "1.0", "Use @bot.command(\"name\", "
                      "hidden=True) instead")
    @property
    def hide_commands(self):
        return self._hide_commands


# Those are shortcuts to send messages directly to someone
# Create dynamic methods for each of the send methods. They're *really*
# repetitive, so generating them with a for loop is not such a bad idea

_proxied_sends = [
    objects.Chat.send,
    objects.Chat.send_photo,
    objects.Chat.send_audio,
    objects.Chat.send_voice,
    objects.Chat.send_video,
    objects.Chat.send_file,
    objects.Chat.send_location,
    objects.Chat.send_sticker,
]

for _proxy in _proxied_sends:
    @utils.wraps(_proxy)
    @utils.deprecated("Bot.%s()" % _proxy.__name__, "1.0",
                      "Use Bot.chat(id).%s() instead." % _proxy.__name__)
    def _wrapper(self, chat, *args, __proxy=_proxy, **kwargs):
        obj = self.chat(chat)

        return __proxy(obj, *args, **kwargs)

    setattr(FrozenBot, _proxy.__name__, _wrapper)


def restore(*args):
    """Restore a FrozenBot instance from pickle"""
    return FrozenBot(*args)
