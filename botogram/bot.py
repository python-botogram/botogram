"""
    botogram.bot
    The actual bot application base

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re
import os
import logging
import gettext

import pkg_resources

from . import api
from . import objects
from . import runner
from . import defaults
from . import components


class Bot:
    """A botogram-made bot"""

    def __init__(self, api_connection):
        self.logger = logging.getLogger("botogram")
        self._configure_logger(self.logger)

        self.api = api_connection

        self.about = ""
        self.owner = ""
        self.hide_commands = ["start"]

        self.before_help = []
        self.after_help = []

        self.process_backlog = False

        self._lang = ""
        self._lang_inst = None

        # Set the default language to english
        self.lang = "en"

        self._components = [defaults.get_default_component(self)]
        self._main_component = components.Component("")

        # Fetch the bot itself's object
        try:
            self.itself = self.api.call("getMe", expect=objects.User)
        except api.APIError as e:
            self.logger.error("Can't connect to Telegram!")
            if e.error_code == 401:
                self.logger.error("The API token seems to be invalid.")
            else:
                self.logger.error("Response from Telegram: %s" % e.description)
            exit(1)

        # This regex will match all commands pointed to this bot
        self._commands_re = re.compile(r'^\/([a-zA-Z0-9_]+)(@' +
                                       self.itself.username+r')?( .*)?$')

    def _configure_logger(self, logger):
        """Configure a logger object"""
        if "BOTOGRAM_DEBUG" in os.environ:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(message)s",
            datefmt='%I:%M:%S'
        )

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    def before_processing(self, func):
        """Register a before processing hook"""
        return self._main_component.add_before_processing_hook(func)

    def process_message(self, func):
        """Add a message processor hook"""
        return self._main_component.add_process_message_hook(func)

    def message_contains(self, string, ignore_case=True, multiple=False):
        """Add a message contains hook"""
        def __(func):
            self._main_component.add_message_contains_hook(func, string,
                                                            ignore_case,
                                                            multiple)
            return func
        return __

    def message_matches(self, regex, flags=0, multiple=False):
        """Add a message matches hook"""
        def __(func):
             self._main_component.add_message_matches_hook(func, regex, flags,
                                                           multiple)
             return func
        return __

    def command(self, name):
        """Register a new command"""
        def __(func):
            self._main_component.add_command(func, name)
            return func
        return __

    def process(self, update):
        """Process an update object"""
        if not isinstance(update, objects.Update):
            raise ValueError("Only Update objects are allowed")

        chain = self._main_component._get_hooks_chain()
        for component in reversed(self._components):
            current_chain = component._get_hooks_chain()
            for i in range(len(chain)):
                chain[i] += current_chain[i]

        # chain[1] should be the commands one
        chain[1].append(defaults.NoCommandsHook(self))

        # Call all the hooks and processors
        # If something returns True, then stop the processing
        for one in chain:
            for hook in one:
                # Get the correct name of the hook
                try:
                    name = hook.botogram.name
                except AttributeError:
                    name = hook.__name__

                self.logger.debug("Processing update #%s with the %s hook...",
                                  update.update_id, name)

                result = self._call(hook, update.message.chat, update.message)
                if result is True:
                    self.logger.debug("Update #%s was just processed by the "
                                      "%s hook.", update.update_id, name)
                    return

        self.logger.debug("No hook actually processed the #%s update.",
                          update.update_id)

    def run(self, workers=2):
        """Run the bot with the multi-process runner"""
        self.logger.info("The botogram runner is booting up.")
        self.logger.info("Press Ctrl+C in order to exit.")

        inst = runner.BotogramRunner(self, workers)
        inst.run()

    def send(self, chat, message, preview=True, reply_to=None, extra=None):
        """Send a message in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send(message, preview, reply_to, extra)

    def send_photo(self, chat, path, caption="", reply_to=None, extra=None):
        """Send a photo in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send_photo(path, caption, reply_to, extra)

    def _(self, message, **args):
        """Translate a string"""
        return self._lang_inst.gettext(message) % args

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Update the bot's language"""
        if lang == self._lang:
            return

        path = pkg_resources.resource_filename("botogram", "i18n/%s.mo" % lang)
        if not os.path.exists(path):
            raise ValueError("Language \"%s\" is not supported by botogram"
                             % lang)

        with open(path, "rb") as f:
            self._lang_inst = gettext.GNUTranslations(f)

        self._lang = lang

    def _get_commands(self):
        """Get all the commands this bot implements"""
        result = {}
        for component in self._components:
            result.update(component._get_commands())
        result.update(self._main_component._get_commands())

        return result

    def _call(self, func, *args, **kwargs):
        """Wrapper for calling user-provided functions"""
        # Put the bot as first argument, if wanted
        if hasattr(func, "botogram") and func.botogram.pass_bot:
            args = (self,) + args

        return func(*args, **kwargs)


def create(api_key, *args, **kwargs):
    """Create a new bot"""
    conn = api.TelegramAPI(api_key)
    return Bot(conn, *args, **kwargs)
