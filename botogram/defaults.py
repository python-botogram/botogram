"""
    botogram.defaults
    Default commands definition

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import utils
from . import objects
from . import components


class StartCommand:

    __name__ = "start_command"

    def __init__(self, bot):
        self.bot = bot
        self._ = bot._

    def __call__(self, chat, message, args):
        message = []
        if self.bot.about:
            message.append(self.bot.about)
        message.append(self._("Use /help to get a list of all the commands."))

        chat.send("\n".join(message))

    def botogram_help_message(self):
        """Get the help message of this command"""
        return "\n".join([
            self._("Start using the bot."),
            self._("This shows a greeting message."),
        ])


class HelpCommand:

    __name__ = "help_command"

    def __init__(self, bot):
        self.bot = bot
        self._ = bot._

    def __call__(self, chat, message, args):
        commands = self.bot._get_commands()
        if len(args) > 1:
            message = [self._("Error: the /help command allows up to one "
                              "argument.")]
        elif len(args) == 1:
            if args[0] in commands:
                message = self.command_message(commands, args[0])
            else:
                message = [self._("Unknow command: /%(name)s.", name=args[0]),
                           self._("Use /help for a list of commands.")]
        else:
            message = self.generic_message(commands)

        chat.send("\n".join(message))

    def botogram_help_message(self):
        """Get the help message of this command"""
        return "\n".join([
            self._("Show this help message."),
            self._("You can also use '/help <command>' to get help about a "
                   "specific command."),
        ])

    def generic_message(self, commands):
        """Generate an help message"""
        message = []

        # Show the about text
        if self.bot.about:
            message.append(self.bot.about)
            message.append("")

        if len(self.bot.before_help):
            message += self.bot.before_help
            message.append("")

        # Show help on commands
        if len(commands) > 0:
            message.append(self._("Available commands:"))
            for name in sorted(commands.keys()):
                # Allow to hide commands in the help message
                if name in self.bot.hide_commands:
                    continue

                func = commands[name]
                # Put a default docstring
                if func.__doc__:
                    original = func.__doc__
                elif hasattr(func, "botogram_help_message"):
                    original = func.botogram_help_message()
                else:
                    original = self._("No description available.")

                docstring = utils.format_docstr(original).split("\n", 1)[0]

                message.append("/%s - %s" % (name, docstring))
            message.append(self._("You can also use '/help <command>' to get "
                                  "help about a specific command."))
        else:
            message.append(self._("No commands available."))

        if len(self.bot.after_help):
            message.append("")
            message += self.bot.after_help

        # Show the owner informations
        if self.bot.owner:
            message.append("")
            message.append(self._("Please contact %(owner)s if you have "
                                  "problems with this bot.",
                                  owner=self.bot.owner))

        return message

    def command_message(self, commands, command):
        """Generate a command's help message"""
        message = []

        func = commands[command]
        if func.__doc__:
            docstring = utils.format_docstr(commands[command].__doc__)
            message.append("/%s - %s" % (command, docstring))
        elif hasattr(func, "botogram_help_message"):
            docstring = utils.format_docstr(func.botogram_help_message())
            message.append("/%s - %s" % (command, docstring))
        else:
            message.append(self._("No help messages for the /%(command)s "
                                  "command.", command=command))

        # Show the owner informations
        if self.bot.owner:
            message.append(" ")
            message.append(self._("Please contact %(owner)s if you have "
                                  "problems with this bot.",
                                  owner=self.bot.owner))

        return message


class NoCommandsHook:

    __name__ = "no_commands_hook"

    def __init__(self, bot):
        self.bot = bot
        self._ = bot._

    def __call__(self, chat, message):
        if message.text is None:
            return

        # First check if a command was invoked
        match = self.bot._commands_re.match(message.text)
        if not match:
            return

        command = match.group(1)
        splitted = message.text.split(" ")
        username = self.bot.itself.username

        mentioned = splitted[0] == "/%s@%s" % (command, username)
        single_user = isinstance(chat, objects.User)
        if mentioned or single_user:
            chat.send("\n".join([
                self._("Unknow command: /%(name)s", name=command),
                self._("Use /help for a list of commands"),
            ]))
            return True


def get_default_component(bot):
    """Get a component with the default stuff"""
    comp = components.Component("botogram")
    comp.add_command(HelpCommand(bot), "help")
    comp.add_command(StartCommand(bot), "start")

    return comp
