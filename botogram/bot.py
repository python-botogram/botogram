"""
    botogram.bot
    The actual bot application base

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re

from . import api
from . import objects
from . import runner
from . import defaults


class Bot:
    """A botogram-made bot"""

    def __init__(self, api_connection):
        self.api = api_connection

        self.about = ""
        self.owner = ""
        self.hide_commands = ["start"]

        self.before_help = []
        self.after_help = []

        self.process_backlog = False

        self._commands = {
            "help": defaults.HelpCommand(self),
            "start": defaults.StartCommand(self),
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
        self._commands_re = re.compile(r'^\/([a-zA-Z0-9_]+)(@' +
                                       self.itself.username+r')?( .*)?$')

    def before_processing(self, func):
        """Register a before processing hook"""
        if not callable(func):
            raise ValueError("A before processing hook must be callable")

        self._before_hooks.append(func)

    def process_message(self, func):
        """Add a message processor hook"""
        if not callable(func):
            raise ValueError("A message processor must be callable")

        self._processors.append(func)
        return func

    def message_contains(self, string, ignore_case=True, multiple=False,
                         func=None):
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
            self.message_matches(regex, flags, multiple, wrapper(func))

            return func

        # If the function was called as a decorator, then return the applier,
        # which will act as a decorator
        # Else, simply apply the function
        if func is None:
            return apply
        apply(func)

    def message_matches(self, regex, flags=0, multiple=False, func=None):
        """Add a message matches hook"""
        def apply(func):
            if not callable(func):
                raise ValueError("A message matches hook must be callable")

            # Save the multiple status
            func._botogram_multiple = multiple

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

    def send(self, chat, message, preview=True, reply_to=None, extra=None):
        """Send a message in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send(message, preview, reply_to, extra)

    def send_photo(self, chat, path, caption="", reply_to=None, extra=None):
        """Send a photo in a chat"""
        obj = objects.GenericChat({"id": chat}, self.api)
        obj.send_photo(path, caption, reply_to, extra)

    def _process_commands(self, chat, message):
        """Hook which process all the commands"""
        if message.text is None:
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
        if message.text is None:
            return

        # Execute all hooks if something matches their pattern
        found = False
        executed = set()
        for regex, funcs in self._message_matches_hooks.items():
            # Support multiple matches per message
            results = regex.finditer(message.text)
            for result in results:
                found = True
                for func in funcs:
                    # Prevents running things multiple times
                    if not func._botogram_multiple and func in executed:
                        continue

                    func(chat, message, result.groups())
                    executed.add(func)

        # If something was found, return true so no other message processors
        # is called
        if found:
            return True


def create(api_key, *args, **kwargs):
    """Create a new bot"""
    conn = api.TelegramAPI(api_key)
    return Bot(conn, *args, **kwargs)
