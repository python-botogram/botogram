"""
    botogram.components
    Definition of the components system

    Copyright (c) 2015 Pietro Albini
    Released under the MIT license
"""

import re
import functools


class Component:
    """A component of a bot"""

    def __init__(self):
        # These will contain all the things registered in this component
        self._commands = {}
        self._processors = []
        self._before_processors = []

    def before_processing(self, func):
        """Register a before processing hook"""
        if not callable(func):
            raise ValueError("A before processing hook must be callable")

        self._before_processors.append(func)
        return func

    def process_message(self, func):
        """Add a message processor hook"""
        if not callable(func):
            raise ValueError("A message processor must be callable")

        self._processors.append(func)
        return func

    def message_contains(self, string, ignore_case=True, multiple=False):
        """Add a message contains hook"""
        def __(func):
            if not callable(func):
                raise ValueError("A message contains hook must be callable")

            regex = r'\b('+string+r')\b'
            flags = re.IGNORECASE if ignore_case else 0

            @functools.wraps(func)
            def wrapped(chat, message, matches):
                return func(chat, message)

            self.message_matches(regex, flags, multiple)(wrapped)
            return func
        return __

    def message_matches(self, regex, flags=0, multiple=False):
        """Apply a message matches hook"""
        def __(func):
            if not callable(func):
                raise ValueError("A message matches hook must be callable")

            @functools.wraps(func)
            def processor(chat, message):
                if message.text is None:
                    return

                compiled = re.compile(regex, flags=flags)
                results = compiled.finditer(message.text)

                found = False
                for result in results:
                    found = True

                    func(chat, message, result.groups())
                    if not multiple:
                        break

                return found

            self._processors.append(processor)
            return func
        return __

    def command(self, name):
        """Register a new command"""
        if name in self._commands:
            raise NameError("The command /%s already exists" % name)

        def __(func):
            if not callable(func):
                raise ValueError("A command processor must be callable")

            self._commands[name] = func
            return func
        return __

    def _get_hooks_chain(self, bot):
        """Get the full hooks chain for this component"""
        chain = [
            self._before_processors,
            self._generate_commands_processors(bot),
            self._processors,
        ]
        return chain

    def _get_commands(self):
        """Get all the commands this component implements"""
        return self._commands

    def _generate_commands_processors(self, bot):
        """Generate a list of commands processors"""
        def base(name, func):
            @functools.wraps(func)
            def __(chat, message):
                # Commands must have a message
                if message.text is None:
                    return

                # Must be this command
                match = bot._commands_re.match(message.text)
                if not match or match.group(1) != name:
                    return

                args = message.text.split(" ")[1:]
                func(chat, message, args)
                return True
            return __

        return [base(name, func) for name, func in self._commands.items()]
