.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _quickstart-better-help:

=====================
A better help command
=====================

When you previously ran the bot, you may have noticed botogram automatically
generated the ``/help`` command along side any commands you have registered.
That's one of the features of botogram, and you can obviously customize it.

.. _quickstart-better-help-about:

Information about the bot
=========================

When someone uses your bot, he might be wondering what it does, or who its
owner is. botogram provides an easy way to add these two pieces of information
to the bot's help message. Add these two lines of code just below the creation
of the bot:

.. code-block:: python
   :emphasize-lines: 2,3

   bot = botogram.create("YOUR-API-KEY")
   bot.about = "This bot is just the one from botogram's tutorial"
   bot.owner = "@yourusername"

Feel free to change the about message and the owner's name as you want. If you
run the bot now, you'll see this information when you issue the ``/help``
command.

.. note::

   The about message will also automatically be added to the ``/start``
   command.

.. _quickstart-better-help-commands:

Help about commands
===================

Usually bots provide commands, and the users of the bot need to know which
commands are available and how to use them. The first part is transparently
handled by botogram, but if you want to provide the commands' description, you
need to provide it.

To apply a description to a command, simply put a docstring to the command's
function:

.. code-block:: python
   :emphasize-lines: 3,4,5

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Say hello to the world!
       This command sends "Hello world" to the current chat
       """
       chat.send("Hello world")

The first non-empty line of the docstring will be shown in the commands list
when issuing ``/help``, and the whole docstring will be shown only if
someone asks for more detailed help on a command. For instance, issuing
``/help hello``, with the command name as an argument.

.. _quickstart-better-help-custom:

Custom help messages
====================

If your bot doesn't execute only commands, but it does something else, it's
better to write what it does in the help message. In order to do so, you can
append messages before and after the commands list, with either the
:py:attr:`botogram.Bot.before_help` or :py:attr:`botogram.Bot.after_help`
attributes. These attributes should contain a list of messages, and each
message will be sent as one paragraph.

In this case, we're going to add a message after the commands, which explains
that the bot will also parse chat messages to send useful information (we're
going to implement this afterwards):

.. code-block:: python
   :emphasize-lines: 3,4,5

   bot.owner = "@yourusername"

   bot.after_help = [
      "This bot also parses the chat in order to send you useful information.",
   ]

.. _quickstart-better-help-source:

Bot's source code until now
===========================

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-API-KEY")
   bot.about = "This bot is just the one from botogram's tutorial"
   bot.owner = "@yourusername"

   bot.after_help = [
      "This bot also parses the chat in order to send you useful information.",
   ]

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Say hello to the world!
       This command sends "Hello world" to the current chat
       """
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()
