"""
    botogram.frozenbot
    A frozen version of the real bot

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import logbook

from . import utils
from . import objects


class FrozenBot:
    """A frozen version of botogram.Bot"""

    def __init__(self, api, about, owner, hide_commands, before_help,
                 after_help, process_backlog, lang, itself, commands_re,
                 components, object_id):

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
        self._botogram_object_id = object_id

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

        print(chains,self._chain)

        # Setup the logger
        self.logger = logbook.Logger('botogram bot')
        utils.configure_logger()

        # Get a fresh Gettext instance
        self._lang_inst = utils.get_language(lang)

        # Prepare the bot representation
        self.itself = itself
        self.itself.set_api(api)

    def __reduce__(self):
        args = (
            self.api, self.about, self.owner, self.hide_commands,
            self.before_help, self.after_help, self.process_backlog,
            self.lang, self.itself, self._commands_re, self._components,
            self._botogram_object_id
        )
        return restore, args

    def __eq__(self, other):
        return self._botogram_object_id == other._botogram_object_id

    # All those methods do nothing, since you aren't allowed to change the
    # hooks a bot has in a frozen instance
    # All of those will be overridden in the Bot class

    def before_processing(self, func):
        """Register a before processing hook"""
        raise RuntimeError("Can't add hooks to a bot at runtime")

    def process_message(self, func):
        """Register a message processor hook"""
        raise RuntimeError("Can't add hooks to a bot at runtime")

    def message_equals(self, string, ignore_case=True):
        """Add a message equals hook"""
        raise RuntimeError("Can't add hooks to a bot at runtime")

    def message_contains(self, string, ignore_case=True, multiple=False):
        """Add a message contains hook"""
        raise RuntimeError("Can't add hooks to a bot at runtime")

    def message_matches(self, regex, flags=0, multiple=False):
        """Add a message matches hook"""
        raise RuntimeError("Can't add hooks to a bot at runtime")

    def command(self, name):
        """Register a new command"""
        raise RuntimeError("Can't add commands to a bot at runtime")

    # Those are shortcuts to send messages directly to someone

    def send(self, chat, message, preview=True, reply_to=None, extra=None):
        """Send a message in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send(message, preview, reply_to, extra)

    def send_photo(self, chat, path, caption="", reply_to=None, extra=None):
        """Send a photo in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send_photo(path, caption, reply_to, extra)

    # Let's process the messages

    def process(self, update):
        """Process an update object"""
        if not isinstance(update, objects.Update):
            raise ValueError("Only Update objects are allowed")

        update.set_api(self.api)  # Be sure to use the correct API object

        for hook in self._chain:
            # Get the correct name of the hook
            try:
                name = hook.botogram.name
            except AttributeError:
                name = hook.__name__

            self.logger.debug("Processing update #%s with the %s hook..." %
                              (update.update_id, name))

            result = self._call(hook, update.message.chat, update.message)
            if result is True:
                self.logger.debug("Update #%s was just processed by the %s "
                                  "hook." % (update.update_id, name))
                return True

        self.logger.debug("No hook actually processed the #%s update." %
                          update.update_id)

        return False

    # This helper manages the translation

    def _(self, message, **args):
        """Translate a string"""
        return self._lang_inst.gettext(message) % args

    # And some internal methods used by botogram

    def _get_commands(self):
        """Get all the commands this bot implements"""
        return self._commands

    def _call(self, func, *args, **kwargs):
        """Wrapper for calling user-provided functions"""
        # Put the bot as first argument, if wanted
        if hasattr(func, "botogram") and func.botogram.pass_bot:
            args = (self,) + args

        return func(*args, **kwargs)


def restore(*args):
    """Restore a FrozenBot instance from pickle"""
    return FrozenBot(*args)
