"""
    botogram.components
    Definition of the components system

    Copyright (c) 2015 Pietro Albini
    Released under the MIT license
"""

import re
import uuid

from . import utils
from . import decorators


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

        self.__before_processors.append(func)

    def add_process_message_hook(self, func):
        """Add a message processor hook"""
        if not callable(func):
            raise ValueError("A message processor must be callable")

        self.__processors.append(func)

    def add_message_equals_hook(self, string, func, ignore_case=True):
        """Add a message equals hook"""
        if not callable(func):
            raise ValueError("A message equals hook must be callable")

        if ignore_case:
            string = string.lower()

        @utils.wraps(func)
        @decorators.pass_bot
        def wrapped(bot, chat, message):
            text = message.text
            if ignore_case:
                text = text.lower()

            if text != string:
                return
            return bot._call(func, chat, message)

        self.add_process_message_hook(wrapped)

    def add_message_contains_hook(self, string, func, ignore_case=True,
                                  multiple=False):
        """Add a message contains hook"""
        if not callable(func):
            raise ValueError("A message contains hook must be callable")

        regex = r'\b('+string+r')\b'
        flags = re.IGNORECASE if ignore_case else 0

        @utils.wraps(func)
        @decorators.pass_bot
        def wrapped(bot, chat, message, matches):
            return bot._call(func, chat, message)

        self.add_message_matches_hook(regex, wrapped, flags, multiple)

    def add_message_matches_hook(self, regex, func, flags=0, multiple=False):
        """Apply a message matches hook"""
        if not callable(func):
            raise ValueError("A message matches hook must be callable")

        @utils.wraps(func)
        @decorators.pass_bot
        def processor(bot, chat, message):
            if message.text is None:
                return

            compiled = re.compile(regex, flags=flags)
            results = compiled.finditer(message.text)

            found = False
            for result in results:
                found = True

                bot._call(func, chat, message, result.groups())
                if not multiple:
                    break

            return found

        self.__processors.append(processor)

    def add_command(self, name, func):
        """Register a new command"""
        if name in self.__commands:
            raise NameError("The command /%s already exists" % name)

        if not callable(func):
            raise ValueError("A command processor must be callable")

        self.__commands[name] = func

    def _add_no_commands_hook(self, func):
        """Register an hook which will be executed when no commands matches"""
        if not callable(func):
            raise ValueError("A no commands hook must be callable")

        self.__no_commands.append(func)

    def _get_hooks_chain(self):
        """Get the full hooks chain for this component"""
        chain = [
            self.__before_processors,
            self.__generate_commands_processors(),
            self.__no_commands,
            self.__processors,
        ]
        return [[self.__wrap_function(f) for f in c] for c in chain]

    def _get_commands(self):
        """Get all the commands this component implements"""
        return self.__commands

    def __generate_commands_processors(self):
        """Generate a list of commands processors"""
        def base(name, func):
            @decorators.pass_bot
            @utils.wraps(func)
            def __(bot, chat, message):
                # Commands must have a message
                if message.text is None:
                    return

                # Must be this command
                match = bot._commands_re.match(message.text)
                if not match or match.group(1) != name:
                    return

                args = message.text.split(" ")[1:]
                bot._call(func, chat, message, args)
                return True
            return __

        return [base(name, func) for name, func in self.__commands.items()]

    def __wrap_function(self, func):
        """Wrap a function, adding to it component-specific things"""
        # This allows us to wrap methods
        real_func = func
        if hasattr(func, "__func__"):
            func = func.__func__

        if not hasattr(func, "botogram"):
            func.botogram = utils.HookDetails(func)

        prefix = self.component_name+"::" if self.component_name else ""

        func.botogram.name = prefix+func.__name__
        func.botogram.component = self

        return real_func
