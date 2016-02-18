"""
    botogram.frozenbot
    A frozen version of the real bot

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import logbook
import inspect

from . import utils
from . import objects


class FrozenBotError(Exception):
    pass


class FrozenBot:
    """A frozen version of botogram.Bot"""

    def __init__(self, api, about, owner, hide_commands, before_help,
                 after_help, process_backlog, lang, itself, commands_re,
                 components, scheduler, main_component_id, bot_id,
                 shared_memory):
        # This attribute should be added with the default setattr, because is
        # needed by the custom setattr
        object.__setattr__(self, "_frozen", False)

        # Restore original content
        self.api = api
        self.about = about
        self.owner = owner
        self.hide_commands = hide_commands
        self.before_help = before_help
        self.after_help = after_help
        self.process_backlog = process_backlog
        self.lang = lang
        self._commands_re = commands_re
        self._components = components
        self._main_component_id = main_component_id
        self._bot_id = bot_id
        self._shared_memory = shared_memory
        self._scheduler = scheduler

        # Rebuild the hooks chain and commands list
        self._commands = components[-1]._get_commands()
        self._chain = []
        chains = components[-1]._get_hooks_chain()
        for component in reversed(components[:-1]):
            self._commands.update(component._get_commands())

            comp_chain = component._get_hooks_chain()
            for i in range(len(chains)):
                chains[i] += comp_chain[i]

        for chain in chains:
            self._chain += chain

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
            self.api, self.about, self.owner, self.hide_commands,
            self.before_help, self.after_help, self.process_backlog,
            self.lang, self.itself, self._commands_re, self._components,
            self._scheduler, self._main_component_id, self._bot_id,
            self._shared_memory,
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

    def command(self, name):
        """Register a new command"""
        raise FrozenBotError("Can't add commands to a bot at runtime")

    def timer(self, interval):
        """Register a new timer"""
        raise FrozenBotError("Can't add timers to a bot at runtime")

    def init_shared_memory(self, func):
        """Add a shared memory initializer"""
        raise FrozenBotError("Can't register a shared memory initializer to a "
                             "bot at runtime")

    # Those are shortcuts to send messages directly to someone

    def send(self, chat, message, preview=True, reply_to=None, syntax=None,
             extra=None):
        """Send a message in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send(message, preview, reply_to, syntax, extra)

    def send_photo(self, chat, path, caption="", reply_to=None, extra=None):
        """Send a photo in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_photo(path, caption, reply_to, extra)

    def send_audio(self, chat, path, duration=None, performer=None, title=None,
                   reply_to=None, extra=None):
        """Send an audio in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_audio(path, duration, performer, title, reply_to, extra)

    def send_voice(self, chat, path, duration=None, reply_to=None, extra=None):
        """Send a voice message in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_voice(path, duration, reply_to, extra)

    def send_video(self, chat, path, duration=None, caption=None,
                   reply_to=None, extra=None):
        """Send a video in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_video(path, duration, caption, reply_to, extra)

    def send_file(self, chat, path, reply_to=None, extra=None):
        """Send a generic file in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_file(path, reply_to, extra)

    def send_location(self, chat, latitude, longitude, reply_to=None,
                      extra=None):
        """Send a generic file in a chat"""
        obj = objects.Chat({"id": chat, "type": ""}, self.api)
        obj.send_location(latitude, longitude, reply_to, extra)

    # Let's process the messages

    def process(self, update):
        """Process an update object"""
        if not isinstance(update, objects.Update):
            raise ValueError("Only Update objects are allowed")

        update.set_api(self.api)  # Be sure to use the correct API object

        for hook in self._chain:
            # Get the correct name of the hook
            name = hook.name
            self.logger.debug("Processing update #%s with the %s hook..." %
                              (update.update_id, name))

            result = hook.call(self, update)
            if result is True:
                self.logger.debug("Update #%s was just processed by the %s "
                                  "hook." % (update.update_id, name))
                return True

        self.logger.debug("No hook actually processed the #%s update." %
                          update.update_id)

        return False

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

    # This helper manages the translation

    def _(self, message, **args):
        """Translate a string"""
        return self._lang_inst.gettext(message) % args

    # And some internal methods used by botogram

    def _get_commands(self):
        """Get all the commands this bot implements"""
        return self._commands

    def _call(self, func, component=None, **available):
        """Wrapper for calling user-provided functions"""
        # Set some default available arguments
        available.setdefault("bot", self)
        if component is not None:
            shared = self._shared_memory.of(self._bot_id, component)
            available.setdefault("shared", shared)

        # Get the correct function signature
        # botogram_original_signature is set while using @utils.wraps
        if hasattr(func, "botogram_original_signature"):
            signature = func.botogram_original_signature
        else:
            signature = inspect.signature(func)

        # Get the wanted arguments
        kwargs = {}
        for name in signature.parameters:
            if name not in available:
                raise TypeError("botogram doesn't know what to provide for %s"
                                % name)
            kwargs[name] = available[name]

        return func(**kwargs)


def restore(*args):
    """Restore a FrozenBot instance from pickle"""
    return FrozenBot(*args)
