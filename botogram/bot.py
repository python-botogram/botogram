"""
    botogram.bot
    The actual bot application base

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re
import logbook
import uuid

import requests.exceptions

from . import api
from . import objects
from . import runner
from . import defaults
from . import components
from . import utils
from . import frozenbot
from . import shared
from . import tasks


class Bot(frozenbot.FrozenBot):
    """A botogram-made bot"""

    def __init__(self, api_connection):
        self.logger = logbook.Logger('botogram bot')

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

    def command(self, name):
        """Register a new command"""
        def __(func):
            self._main_component.add_command(name, func, _from_main=True)
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

    def freeze(self):
        """Return a frozen instance of the bot"""
        chains = components.merge_chains(self._main_component,
                                         *self._components)

        # Get the list of commands for the bot
        commands = self._components[-1]._get_commands()
        for component in reversed(self._components[:-1]):
            commands.update(component._get_commands())
        commands.update(self._main_component._get_commands())

        return frozenbot.FrozenBot(self.api, self.about, self.owner,
                                   self.hide_commands, self.before_help,
                                   self.after_help, self.process_backlog,
                                   self.lang, self.itself, self._commands_re,
                                   commands, chains, self._scheduler,
                                   self._main_component._component_id,
                                   self._bot_id, self._shared_memory)

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

    def _get_commands(self):
        """Get all the commands this bot implements"""
        result = {}
        for component in self._components:
            result.update(component._get_commands())
        result.update(self._main_component._get_commands())

        return result


def create(api_key, *args, **kwargs):
    """Create a new bot"""
    conn = api.TelegramAPI(api_key)
    return Bot(conn, *args, **kwargs)


def channel(name, api_key):
    """Get a representation of a channel"""
    conn = api.TelegramAPI(api_key)

    obj = objects.Chat({"id": 0, "type": "channel", "username": name}, conn)
    return obj
