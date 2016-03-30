"""
    botogram.defaults
    Default commands definition

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import utils
from . import components
from . import decorators


class DefaultComponent(components.Component):
    """This component contains all the goodies botogram provides by default"""

    component_name = "botogram"

    def __init__(self):
        self.add_command("start", self.start_command)
        self.add_command("help", self.help_command)

        self._add_no_commands_hook(self.no_commands_hook)

    # /start command

    def start_command(self, bot, chat):
        message = []
        if bot.about:
            message.append(bot.about)
            message.append("")
        message.append(bot._("Use /help to get a list of all the commands."))

        chat.send("\n".join(message), syntax="html")

    @decorators.help_message_for(start_command)
    def _start_command_help(bot):
        return "\n".join([
            bot._("Start using the bot."),
            bot._("This shows a greeting message."),
        ])

    # /help command

    def help_command(self, bot, chat, args):
        commands = bot._get_commands()
        if len(args) > 1:
            message = [bot._("<b>Error!</b> The <code>/help</code> command "
                             "allows up to one argument.")]
        elif len(args) == 1:
            if args[0] in commands:
                message = self._help_command_message(bot, commands, args[0])
            else:
                message = [bot._("<b>Unknown command:</b> "
                                 "<code>/%(name)s</code>",
                                 name=args[0]),
                           bot._("Use /help to get a list of the commands.")]
        else:
            message = self._help_generic_message(bot, commands)

        chat.send("\n".join(message), syntax="html")

    def _help_generic_message(self, bot, commands):
        """Generate an help message"""
        message = []

        # Show the about text
        if bot.about:
            message.append(bot.about)
            message.append("")

        if len(bot.before_help):
            message += bot.before_help
            message.append("")

        # Show help on commands
        if len(commands) > 0:
            message.append(bot._("<b>This bot supports those commands:</b>"))
            for name in sorted(commands.keys()):
                # Allow to hide commands in the help message
                if name in bot.hide_commands:
                    continue

                func = commands[name]
                docstring = utils.docstring_of(func, bot, format=True) \
                                 .split("\n", 1)[0]
                message.append("/%s <code>-</code> %s" % (name, docstring))
            message.append("")
            message.append(bot._("You can also use <code>/help &lt;command&gt;"
                                 "</code> to get help about a specific "
                                 "command."))
        else:
            message.append(bot._("<i>This bot has no commands.</i>"))

        if len(bot.after_help):
            message.append("")
            message += bot.after_help

        # Show the owner informations
        if bot.owner:
            message.append("")
            message.append(bot._("Please contact %(owner)s if you have "
                                 "problems with this bot.",
                                 owner=bot.owner))

        return message

    def _help_command_message(self, bot, commands, command):
        """Generate a command's help message"""
        message = []

        func = commands[command]
        docstring = utils.docstring_of(func, bot, format=True)
        message.append("/%s <code>-</code> %s" % (command, docstring))

        # Show the owner informations
        if bot.owner:
            message.append(" ")
            message.append(bot._("Please contact %(owner)s if you have "
                                 "problems with this bot.",
                                 owner=bot.owner))

        return message

    @decorators.help_message_for(help_command)
    def _help_command_help(bot):
        """Get the help message of this command"""
        return "\n".join([
            bot._("Show this help message."),
            bot._("You can also use <code>/help &lt;command&gt;</code> to get "
                  "help about a specific command."),
        ])

    # An hook which displays "Command not found" if needed

    def no_commands_hook(self, bot, chat, message):
        if message.text is None:
            return

        # First check if a command was invoked
        match = bot._commands_re.match(message.text)
        if not match:
            return

        command = match.group(1)
        splitted = message.text.split(" ")
        username = bot.itself.username

        mentioned = splitted[0] == "/%s@%s" % (command, username)
        single_user = chat.type == "private"
        if mentioned or single_user:
            chat.send("\n".join([
                bot._("<b>Unknown command:</b> <code>/%(name)s</code>",
                      name=command),
                bot._("Use /help to get a list of the commands."),
            ]), syntax="html")
            return True
