.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _tutorial-better-help:

~~~~~~~~~~~~~~~~~~~~~
A better help command
~~~~~~~~~~~~~~~~~~~~~

When you previously ran the bot, you may have noticed botogram automatically
generated the ``/help`` command, with all the commands you have registered and
the builtin ones. That's one of the features of botogram, and you can obviusly
customize it.

.. _tutorial-better-help-about:

==========================
Informations about the bot
==========================

When someone uses your bot, he might be wondering what it does, or what's the
owner of it. botogram provides an easy way to add these two pieces of
information to the bot's help message. Add these two lines of code just below
the creation of the bot:

.. code-block:: python
   :emphasize-lines: 2,3

   bot = botogram.create("YOUR-API-KEY")
   bot.about = "This bot is just the one from the botogram's tutorial"
   bot.owner = "@yourusername"

Feel free to change the about message and the owner's name as you want. If you
try to run the bot now, you'll see these information when you issue the
command.

.. note::

   The about message will be also automatically added to the ``/start``
   command.

.. _tutorial-better-help-commands:

===================
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

The first non-empty line of the docstring will be showed in the commands list
available issuing ``/help``, and the whole docstring will be showed only if
someone asks more detailed help for a command, issuing ``/help`` with the
command name as argument.

.. _tutorial-better-help-custom:

====================
Custom help messages
====================

If your bot doesn't execute only commands, but it does something else, it's
better to write what it does in the help message. In order to do so, you can
append messages before and after the commands list, with either the
:py:attr:`botogram.Bot.before_help` or :py:attr:`botogram.Bot.after_help`
attributes. These attributes should contain a list of messages, and each
message will be sent in one different line.

In this case, we're going to add a message after the commands, which explains
that the bot will also parse chat messages to send useful informations (we're
going to implement this afterwards):

.. code-block:: python
   :emphasize-lines: 3,4,5

   bot.owner = "@yourusername"

   bot.after_help = [
      "This bot also parses the chat in order to send you useful informations.",
   ]

.. _tutorial-better-help-source:

===========================
Bot's source code until now
===========================

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-API-KEY")
   bot.about = "This bot is just the one from the botogram's tutorial"
   bot.owner = "@yourusername"

   bot.after_help = [
      "This bot also parses the chat in order to send you useful informations.",
   ]

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Say hello to the world!
       This command sends "Hello world" to the current chat
       """
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()
