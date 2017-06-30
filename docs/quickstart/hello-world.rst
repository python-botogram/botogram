.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _quickstart-hello-world:

============================
A simple Hello world command
============================

Every time a programmer learns a new programming language or a new framework,
it's tradition to write a "hello world" program. In this case, we'll add a
``/hello`` command, which will simply reply "Hello world" in the chat or
group chat.

In botogram, a command is a function decorated with the
:py:meth:`botogram.Bot.command` decorator. So, let's add this snippet:

.. code-block:: python
   :emphasize-lines: 3,4,5

   bot = botogram.create("YOUR-API-KEY")

   @bot.command("hello")
   def hello_command(chat, message, args):
       pass

The first line is a decorator, which will register the function under it as
the ``/hello`` command. The function can have an arbitrary name, and it may
accept any of these three :ref:`tricks-dynamic-arguments`:

* The chat where the command was issued (an instance of
  :py:class:`botogram.Chat`)
* The representation of the sent message (an instance of
  :py:class:`botogram.Message`)
* The list of the parsed command arguments

So, we'd like to reply with "Hello world" when someone issue the command.
Thankfully, there is an handy method on the chat object:

.. code-block:: python
   :emphasize-lines: 3

   @bot.command("hello")
   def hello_command(chat, message, args):
       chat.send("Hello world")

Perfect, now the command is ready! Try to run the bot, and send it ``/hello``:
it will reply with "Hello world".

.. _quickstart-hello-world-source:

Bot's source code until now
===========================

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-API-KEY")

   @bot.command("hello")
   def hello_command(chat, message, args):
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()
