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

import re
import logbook
import uuid

import requests.exceptions

from . import api
from . import callbacks
from . import objects
from . import runner
from . import defaults
from . import components
from . import utils
from . import frozenbot
from . import shared
from . import tasks
from . import messages


class Bot(frozenbot.FrozenBot):
    """A botogram-made bot"""

    def __init__(self, api_connection):
        self.logger = logbook.Logger('botogram bot')

        self.api = api_connection

        self.about = ""
        self.owner = ""

        self.before_help = []
        self.after_help = []

        self.link_preview_in_help = True

        self.process_backlog = False

        self.validate_callback_signatures = True

        self._lang = ""
        self._lang_inst = None
        self.override_i18n = {}

        # Support for the old, deprecated bot.hide_commands
        self._hide_commands = []

        # Set the default language to english
        self.lang = "en"

        self._components = []
        self._main_component = components.Component("")
        self._main_component_id = self._main_component._component_id

        # Setup shared memory
        self._shared_memory = shared.SharedMemory()

        # Register bot's shared memory initializers
        inits = self._main_component._get_chains()["memory_preparers"][0]
        maincompid = self._main_component._component_id
        self._shared_memory.register_preparers_list(maincompid, inits)

        # Setup the scheduler
        self._scheduler = tasks.Scheduler()

        # Initialize the list of update processors
        self._update_processors = {}
        self.register_update_processor("message", messages.process_message)
        self.register_update_processor("edited_message",
                                       messages.process_edited_message)
        self.register_update_processor("channel_post",
                                       messages.process_channel_post)
        self.register_update_processor("edited_channel_post",
                                       messages.process_channel_post_edited)
        self.register_update_processor("callback_query", callbacks.process)

        self._bot_id = str(uuid.uuid4())

        self.use(defaults.DefaultComponent())
        self.use(self._main_component, only_init=True)

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
        except requests.exceptions.ConnectionError:
            self.logger.error("Can't reach Telegram servers! Are you sure "
                              "you're connected to the internet?")
            exit(1)

        # This regex will match all commands pointed to this bot
        self._commands_re = re.compile(r'^\/([a-zA-Z0-9_]+)(@' +
                                       self.itself.username + r')?( .*)?$')

    def __reduce__(self):
        # Use the standard __reduce__
        return object.__reduce__(self)

    def __setattr__(self, name, value):
        # Warn about disabled callback validation
        if name == "validate_callback_signatures" and not value:
            self.logger.warn("Your code disabled signature validation for "
                             "callbacks!")
            self.logger.warn("This can cause security issues. Please enable "
                             "it again.")

        # Use the standard __setattr__
        return object.__setattr__(self, name, value)

    def before_processing(self, func):
        """Register a before processing hook"""
        self._main_component.add_before_processing_hook(func)
        return func

    def process_message(self, func):
        """Add a message processor hook"""
        self._main_component.add_process_message_hook(func)
        return func

    def message_equals(self, string, ignore_case=True):
        """Add a message equals hook"""
        def __(func):
            self._main_component.add_message_equals_hook(string, func,
                                                         ignore_case)
            return func
        return __

    def message_contains(self, string, ignore_case=True, multiple=False):
        """Add a message contains hook"""
        def __(func):
            self._main_component.add_message_contains_hook(string, func,
                                                           ignore_case,
                                                           multiple)
            return func
        return __

    def message_matches(self, regex, flags=0, multiple=False):
        """Add a message matches hook"""
        def __(func):
            self._main_component.add_message_matches_hook(regex, func, flags,
                                                          multiple)
            return func
        return __

    def message_edited(self, func):
        """Add a message edited hook"""
        self._main_component.add_message_edited_hook(func)
        return func

    def channel_post(self, func):
        """Add a channel post hook"""
        self._main_component.add_channel_post_hook(func)
        return func

    def channel_post_edited(self, func):
        """Add a edited channel post hook"""
        self._main_component.add_channel_post_edited_hook(func)
        return func

    def command(self, name, hidden=False, order=0):
        """Register a new command"""
        def __(func):
            self._main_component.add_command(name, func, hidden,
                                             order=order, _from_main=True)
            return func
        return __

    def callback(self, name):
        """Register a new callback"""
        def __(func):
            self._main_component.add_callback(name, func)
            return func
        return __

    def timer(self, interval):
        """Register a new timer"""
        def __(func):
            self._main_component.add_timer(interval, func)
            return func
        return __

    def prepare_memory(self, func):
        """Register a shared memory's preparer"""
        self._main_component.add_memory_preparer(func)
        return func

    @utils.deprecated("@bot.init_shared_memory", "1.0", "Rename the decorator "
                      "to @bot.prepare_memory")
    def init_shared_memory(self, func):
        """This decorator is deprecated, and it calls @prepare_memory"""
        return self.prepare_memory(func)

    def chat_unavailable(self, func):
        """Add a chat unavailable hook"""
        self._main_component.add_chat_unavailable_hook(func)
        return func

    def use(self, *components, only_init=False):
        """Use the provided components in the bot"""
        for component in components:
            if not only_init:
                self.logger.debug("Component %s just loaded into the bot" %
                                  component.component_name)
                self._components.append(component)

            # Register initializers for the shared memory
            chains = component._get_chains()
            compid = component._component_id
            preparers = chains["memory_preparers"][0]
            self._shared_memory.register_preparers_list(compid, preparers)

            # Register tasks
            self._scheduler.register_tasks_list(chains["tasks"][0])

    def process(self, update):
        """Process an update object"""
        # Updates are always processed in a frozen instance
        # This way there aren't inconsistencies between the runner and manual
        # update processing
        frozen = self.freeze()
        return frozen.process(update)

    def run(self, workers=2):
        """Run the bot with the multi-process runner"""
        inst = runner.BotogramRunner(self, workers=workers)
        inst.run()

    def register_update_processor(self, kind, processor):
        """Register a new update processor"""
        if kind in self._update_processors:
            self.logger.warn("Your code replaced the default update processor "
                             "for '%s'!" % kind)
            self.logger.warn("If you want botogram to handle those updates "
                             "natively remove your processor.")

        self._update_processors[kind] = processor

    def freeze(self):
        """Return a frozen instance of the bot"""
        chains = components.merge_chains(self._main_component,
                                         *self._components)

        return frozenbot.FrozenBot(self.api, self.about, self.owner,
                                   self._hide_commands, self.before_help,
                                   self.after_help, self.link_preview_in_help,
                                   self.validate_callback_signatures,
                                   self.process_backlog, self.lang,
                                   self.itself, self._commands_re,
                                   self._commands, chains, self._scheduler,
                                   self._main_component._component_id,
                                   self._bot_id, self._shared_memory,
                                   self._update_processors, self.override_i18n)

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        """Update the bot's language"""
        if lang == self._lang:
            return

        self._lang_inst = utils.get_language(lang)
        self._lang = lang

    @property
    def _commands(self):
        """Get all the commands this bot implements"""
        # This is marked as a property so the available_commands method becomes
        # dynamic (it's static on FrozenBot instead)
        commands = self._components[-1]._get_commands()
        for component in reversed(self._components[:-1]):
            commands.update(component._get_commands())
        commands.update(self._main_component._get_commands())

        result = {}
        for name, command in commands.items():
            result[name] = command.for_bot(self)
        return result

    # These functions allows to use the old, deprecated bot.hide_commands

    @property
    @utils.deprecated("bot.hide_commands", "1.0", "Use @bot.command(\"name\", "
                      "hidden=True) instead")
    def hide_commands(self):
        return self._hide_commands

    @hide_commands.setter
    @utils.deprecated("bot.hide_commands", "1.0", "Use @bot.command(\"name\", "
                      "hidden=True) instead", back=1)
    def hide_commands(self, value):
        self._hide_commands = value


def create(api_key, *args, **kwargs):
    """Create a new bot"""
    conn = api.TelegramAPI(api_key)
    return Bot(conn, *args, **kwargs)


def channel(name, api_key):
    """Get a representation of a channel"""
    conn = api.TelegramAPI(api_key)

    obj = conn.call("getChat", {"chat_id": name}, expect=objects.Chat)
    return obj
