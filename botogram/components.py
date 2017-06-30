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
        self.__callbacks = {}
        self.__processors = []
        self.__no_commands = []
        self.__before_processors = []
        self.__memory_preparers = []
        self.__timers = []
        self.__chat_unavailable_hooks = []
        self.__messages_edited_hooks = []
        self.__channel_post_hooks = []
        self.__channel_post_edited_hooks = []

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

    def add_command(self, name, func, hidden=False, order=0, _from_main=False):
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
            "order": order,
        })
        command = commands.Command(hook)
        self.__commands[name] = command

    def add_callback(self, name, func):
        """Add a new callback"""
        if name in self.__callbacks:
            raise NameError("The callback %s already exists" % name)

        if not callable(func):
            raise ValueError("A callback must be callable")

        hook = hooks.CallbackHook(func, self, {
            "name": name,
        })
        self.__callbacks[name] = hook

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

    def add_channel_post_hook(self, func):
        """Add a channel post hook"""
        if not callable(func):
            raise ValueError("A channel post hook must be callable")

        hook = hooks.ChannelPostHook(func, self)
        self.__channel_post_hooks.append(hook)

    def add_channel_post_edited_hook(self, func):
        """Add an edited channel post hook"""
        if not callable(func):
            raise ValueError("A edited channel post hook must be callable")

        hook = hooks.EditedChannelPostHook(func, self)
        self.__channel_post_edited_hooks.append(hook)

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
            "channel_post": [self.__channel_post_hooks],
            "channel_post_edited": [self.__channel_post_edited_hooks],
            "callbacks": [[
                self.__callbacks[name]
                for name in sorted(self.__callbacks.keys())
            ]],
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
