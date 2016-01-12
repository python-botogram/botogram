"""
    botogram.components
    Definition of the components system

    Copyright (c) 2015-2016 Pietro Albini
    Released under the MIT license
"""

import uuid

from . import utils
from . import tasks
from . import hooks


class Component:
    """A component of a bot"""

    component_name = None

    def __new__(cls, *args, **kwargs):
        # Here __new__ is used because this way subclasses can define their
        # own __init__ without explicitly calling the Component one
        self = super(Component, cls).__new__(cls)

        self.__commands = {}
        self.__processors = []
        self.__no_commands = []
        self.__before_processors = []
        self.__shared_inits = []
        self.__timers = []

        self._component_id = str(uuid.uuid4())

        if cls.component_name is None:
            self.component_name = cls.__name__

        return self

    def __init__(self, name=None):
        # This is a default, completly overrideable init
        if name is not None:
            self.component_name = name

    def add_before_processing_hook(self, func):
        """Register a before processing hook"""
        if not callable(func):
            raise ValueError("A before processing hook must be callable")

        hook = hooks.BeforeProcessingHook(func, self)
        self.__before_processors.append(hook)

    def add_process_message_hook(self, func):
        """Add a message processor hook"""
        if not callable(func):
            raise ValueError("A message processor must be callable")

        hook = hooks.ProcessMessageHook(func, self)
        self.__processors.append(hook)

    def add_message_equals_hook(self, string, func, ignore_case=True):
        """Add a message equals hook"""
        if not callable(func):
            raise ValueError("A message equals hook must be callable")

        hook = hooks.MessageEqualsHook(func, self, {
            "ignore_case": ignore_case,
            "string": string,
        })
        self.__processors.append(hook)

    def add_message_contains_hook(self, string, func, ignore_case=True,
                                  multiple=False):
        """Add a message contains hook"""
        if not callable(func):
            raise ValueError("A message contains hook must be callable")

        hook = hooks.MessageContainsHook(func, self, {
            "ignore_case": ignore_case,
            "multiple": multiple,
            "string": string,
        })
        self.__processors.append(hook)

    def add_message_matches_hook(self, regex, func, flags=0, multiple=False):
        """Apply a message matches hook"""
        if not callable(func):
            raise ValueError("A message matches hook must be callable")

        hook = hooks.MessageMatchesHook(func, self, {
            "flags": flags,
            "multiple": multiple,
            "regex": regex,
        })
        self.__processors.append(hook)

    def add_command(self, name, func, _from_main=False):
        """Register a new command"""
        if name in self.__commands:
            raise NameError("The command /%s already exists" % name)

        if not callable(func):
            raise ValueError("A command processor must be callable")

        if name[0] == "/":
            go_back = -3 if _from_main else -2
            utils.warn(go_back, "Command names shouldn't be prefixed with a "
                       "slash. It's done automatically.")

        hook = hooks.CommandHook(func, self, {
            "name": name,
        })
        self.__commands[name] = hook

    def add_timer(self, interval, func):
        """Register a new timer"""
        if not callable(func):
            raise ValueError("A timer must be callable")

        hook = hooks.TimerHook(func, self)
        job = tasks.TimerTask(interval, hook)

        self.__timers.append(job)

    def add_shared_memory_initializer(self, func):
        """Add a new shared memory's initializer"""
        if not callable(func):
            raise ValueError("A shared memory initializer must be callable")

        hook = hooks.SharedMemoryInitializerHook(func, self)
        self.__shared_inits.append(hook)

    def _add_no_commands_hook(self, func):
        """Register an hook which will be executed when no commands matches"""
        if not callable(func):
            raise ValueError("A no commands hook must be callable")

        hook = hooks.NoCommandsHook(func, self)
        self.__no_commands.append(hook)

    def _get_hooks_chain(self):
        """Get the full hooks chain for this component"""
        return [
            self.__before_processors[:],
            [self.__commands[name] for name in sorted(self.__commands.keys())],
            self.__no_commands[:],
            self.__processors[:],
        ]

    def _get_commands(self):
        """Get all the commands this component implements"""
        return self.__commands

    def _get_shared_memory_inits(self):
        """Get a list of all the shared memory initializers"""
        return self.__shared_inits

    def _get_timers(self):
        """Get a list of all the timers"""
        return self.__timers
