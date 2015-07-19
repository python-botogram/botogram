"""
    botogram.defaults
    Default commands definition

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import utils


class StartCommand:
    """Start using the bot.
    It shows a greeting message.
    """

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, chat, message, args):
        message = []
        if self.bot.about:
            message.append(self.bot.about)
        message.append("Use /help to get a list of all the commands.")

        chat.send("\n".join(message))


class HelpCommand:
    """Show this help message
    You can also use '/help <command>' to get help about a command.
    """

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, chat, message, args):
        commands = self.bot._commands
        if len(args) > 1:
            message = ["Error: the /help command allows up to one argument."]
        elif len(args) == 1:
            if args[0] in commands:
                message = self.command_message(commands, args[0])
            else:
                message = ["Error: Unknow command: /%s" % args[0],
                           "Use /help for a list of commands."]
        else:
            message = self.generic_message(commands)

        chat.send("\n".join(message))

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
            message.append("Available commands:")
            for name in sorted(commands.keys()):
                # Allow to hide commands in the help message
                if name in self.bot.hide_commands:
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

        if len(self.bot.after_help):
            message.append("")
            message += self.bot.after_help

        # Show the owner informations
        if self.bot.owner:
            message.append("")
            message.append("Please contact %s if you have problems with "
                           "this bot." % self.bot.owner)

        return message

    def command_message(self, commands, command):
        """Generate a command's help message"""
        message = []

        if commands[command].__doc__:
            docstring = utils.format_docstr(commands[command].__doc__)
            message.append("/%s - %s" % (command, docstring))
        else:
            message.append("No help messages for the /%s command." % command)

        # Show the owner informations
        if self.bot.owner:
            message.append(" ")
            message.append("Please contact %s if you have problems with "
                           "this bot." % self.bot.owner)

        return message
