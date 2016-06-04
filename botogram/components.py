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
from . import commands


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
        self.__memory_preparers = []
        self.__timers = []
        self.__chat_unavailable_hooks = []
        self.__messages_edited_hooks = []

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

    def add_command(self, name, func, hidden=False, _from_main=False):
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
            "hidden": hidden,
        })
        command = commands.Command(hook)
        self.__commands[name] = command

    def add_timer(self, interval, func):
        """Register a new timer"""
        if not callable(func):
            raise ValueError("A timer must be callable")

        hook = hooks.TimerHook(func, self)
        job = tasks.TimerTask(interval, hook)

        self.__timers.append(job)

    def add_memory_preparer(self, func):
        """Add a new shared memory's initializer"""
        if not callable(func):
            raise ValueError("A memory preparer must be callable")

        hook = hooks.MemoryPreparerHook(func, self)
        self.__memory_preparers.append(hook)

    @utils.deprecated("Component.add_shared_memory_initializer", "1.0",
                      "Rename the method to Component.add_memory_preparer")
    def add_shared_memory_initializer(self, func):
        """This method is deprecated, and it calls add_memory_preparer"""
        self.add_memory_preparer(func)

    def add_chat_unavailable_hook(self, func):
        """Add a new chat unavailable hook"""
        if not callable(func):
            raise ValueError("A chat unavailable hook must be callable")

        hook = hooks.ChatUnavailableHook(func, self)
        self.__chat_unavailable_hooks.append(hook)

    def add_message_edited_hook(self, func):
        """Add a new edited message hook"""
        if not callable(func):
            raise ValueError("A message edited hook must be callable")

        hook = hooks.MessageEditedHook(func, self)
        self.__messages_edited_hooks.append(hook)

    def _add_no_commands_hook(self, func):
        """Register an hook which will be executed when no commands matches"""
        if not callable(func):
            raise ValueError("A no commands hook must be callable")

        hook = hooks.NoCommandsHook(func, self)
        self.__no_commands.append(hook)

    def _get_chains(self):
        """Get the full hooks chain for this component"""
        messages = [
            self.__before_processors[:],
            [self.__commands[name]._hook
                for name in sorted(self.__commands.keys())],
            self.__no_commands[:],
            self.__processors[:],
        ]
        return {
            "messages": messages,
            "memory_preparers": [self.__memory_preparers],
            "tasks": [self.__timers],
            "chat_unavalable_hooks": [self.__chat_unavailable_hooks],
            "messages_edited": [self.__messages_edited_hooks],
        }

    def _get_commands(self):
        """Get all the commands this component implements"""
        return self.__commands


def merge_chains(main, *components):
    """Merge multiple chains returned by the components"""
    merged = {}
    components = [main] + list(reversed(components))

    # First of all, merge all the subchains of the different components
    # together -- This is a separate step so the order is preserved
    for component in components:
        macrochains = component._get_chains()
        for kind, chains in macrochains.items():
            if kind not in merged:
                merged[kind] = []

            for i, chain in enumerate(chains):
                try:
                    merged[kind][i] += chain
                except IndexError:
                    merged[kind].append(chain[:])

    # Then merge all the subchains together
    result = {}
    for kind, chains in merged.items():
        result[kind] = []
        for chain in chains:
            result[kind] += chain

    return result
