"""
    botogram.bot
    The actual bot application base

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re

from . import api
from . import objects
from . import utils
from . import runner


class Bot:
    """A botogram-made bot"""

    def __init__(self, api_connection, help=True):
        self.api = api_connection

        self.about = ""
        self.owner = ""
        self.hide_from_help = ["start"]

        self._commands = {
            "help": self._default_help_command,
            "start": self._default_start_command,
        }
        self._processors = [
            self._process_commands,
            self._process_message_matches
        ]
        self._message_matches_hooks = {}
        self._before_hooks = []

        # You can override these commands one time
        self._builtin_commands = list(self._commands.keys())

        # Fetch the bot itself's object
        self.itself = self.api.call("getMe", expect=objects.User)

        # This regex will match all commands pointed to this bot
        self._commands_re = re.compile(r'^\/([a-zA-Z0-9_]+)(@'+self.itself.username+r')?( .*)?$')

    def before_processing(self, func):
        """Register a before processing hook"""
        if not callable(func):
            raise ValueError("A before processing hook must be callable")

        self._before_hooks.append(func)

    def process_messages(self, func):
        """Add a message processor hook"""
        if not callable(func):
            raise ValueError("A message processor must be callable")

        self._processors.append(func)
        return func

    def message_contains(self, string, ignore_case=True, func=None):
        """Add a message contains hook"""
        def apply(func):
            if not callable(func):
                raise ValueError("A message contains hook must be callable")

            regex = r'\b('+string+r')\b'
            flags = re.IGNORECASE if ignore_case else 0

            # Ignore the matches argument
            def wrapper(func):
                def __(chat, message, matches):
                    return func(chat, message)
                return __

            # Register this as a regex
            self.message_matches(regex, flags, wrapper(func))

            return func

        # If the function was called as a decorator, then return the applier,
        # which will act as a decorator
        # Else, simply apply the function
        if func is None:
            return apply
        apply(func)

    def message_matches(self, regex, flags=0, func=None):
        """Add a message matches hook"""
        def apply(func):
            if not callable(func):
                raise ValueError("A message matches hook must be callable")

            compiled = re.compile(regex, flags=flags)
            if compiled not in self._message_matches_hooks:
                self._message_matches_hooks[compiled] = []
            self._message_matches_hooks[compiled].append(func)

            return func

        # If the function was called as a decorator, then return the applier,
        # which will act as a decorator
        # Else, simply apply the function
        if func is None:
            return apply
        apply(func)

    def command(self, name, func=None):
        """Register a new command"""
        # You can override all the builtin commands
        if name in self._commands and name not in self._builtin_commands:
            raise NameError("The command /%s already exists" % name)

        def apply(func):
            if not callable(func):
                raise ValueError("A command processor must be callable")

            self._commands[name] = func

            # This isn't a builtin command anymore...
            if name in self._builtin_commands:
                self._builtin_commands.remove(name)

            return func

        # If the function is called as a decorator, then return the applier,
        # which will act as a decorator
        # Else, simply apply the function
        if func is None:
            return apply
        apply(func)

    def process(self, update):
        """Process an update object"""
        if not isinstance(update, objects.Update):
            raise ValueError("Only Update objects are allowed")

        # Call all the hooks and processors
        # If something returns True, then stop the processing
        for hook in self._before_hooks+self._processors:
            result = hook(update.message.chat, update.message)
            if result is True:
                return

    def run(self, workers=2):
        """Run the bot with the multi-process runner"""
        print("Botogram runner started -- Exit with Ctrl+C")
        inst = runner.BotogramRunner(self, workers)
        inst.run()

    def _process_commands(self, chat, message):
        """Hook which process all the commands"""
        if not hasattr(message, "text"):
            return

        match = self._commands_re.match(message.text)
        if not match:
            return

        command = match.group(1)
        splitted = message.text.split(" ")
        args = splitted[1:]

        # This detects if the bot is called with a mention
        mentioned = False
        if splitted[0] == "/%s@%s" % (command, self.itself.username):
            mentioned = True

        commands = self._commands
        if command in commands:
            commands[command](chat, message, args)
            return True
        # Match single-user chat or command pointed to this
        # specific bot -- /command@botname
        elif isinstance(chat, objects.User) or mentioned:
            chat.send("\n".join([
                "Unknow command /%s." % command,
                "Use /help for a list of commands."
            ]))

    def _process_message_matches(self, chat, message):
        """Hook which processes all the message matches hooks"""
        if not hasattr(message, "text"):
            return

        # Execute all hooks if something matches their pattern
        found = False
        for regex, funcs in self._message_matches_hooks.items():
            # Support multiple matches per message
            results = regex.finditer(message.text)
            for result in results:
                found = True
                for func in funcs:
                    func(chat, message, result.groups())

        # If something was found, return true so no other message processors
        # is called
        if found:
            return True

    def _default_start_command(self, chat, message, args):
        """Start using the bot.
        It shows a greeting message.
        """
        message = []
        if self.about:
            message.append(self.about)
        message.append("Use /help to get a list of all the commands")

        chat.send("\n".join(message))

    def _default_help_command(self, chat, message, args):
        """Show this help message
        You can also use '/help <command>' to get help about a command.
        """
        commands = self._commands
        if len(args) > 1:
            message = ["Error: the /help command allows up to one argument."]
        elif len(args) == 1:
            if args[0] in commands:
                message = self._command_help_message(commands, args[0])
            else:
                message = ["Error: Unknow command: /%s" % args[0],
                           "Use /help for a list of commands."]
        else:
            message = self._generic_help_message(commands)

        chat.send("\n".join(message))

    def _generic_help_message(self, commands):
        """Generate an help message"""
        message = []

        # Show the about text
        if self.about:
            message.append(self.about)
            message.append("")

        # Show help on commands
        if len(self._commands) > 0:
            message.append("Available commands:")
            for name in sorted(commands.keys()):
                # Allow to hide commands in the help message
                if name in self.hide_from_help:
                    continue

                func = commands[name]
                # Put a default docstring
                if not func.__doc__:
                    docstring = "No description available."
                else:
                    docstring = func.__doc__.strip().split("\n", 1)[0]

                message.append("/%s - %s" % (name, docstring))
            message.append("Use /help <command> if you need help about a "
                           "specific command.")
        else:
            message.append("No commands available.")

        # Show the owner informations
        if self.owner:
            message.append(" ")
            message.append("Please contact %s if you have problems with "
                           "this bot." % self.owner)

        return message

    def _command_help_message(self, commands, command):
        """Generate a command's help message"""
        message = []

        if commands[command].__doc__:
            docstring = utils.format_docstr(commands[command].__doc__)
            message.append("/%s - %s" % (command, docstring))
        else:
            message.append("No help messages for the /%s command." % command)

        # Show the owner informations
        if self.owner:
            message.append(" ")
            message.append("Please contact %s if you have problems with "
                           "this bot" % self.owner)

        return message


def create(api_key, *args, **kwargs):
    """Create a new bot"""
    conn = api.TelegramAPI(api_key)
    return Bot(conn, *args, **kwargs)
