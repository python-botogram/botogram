.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _bot-structure:

===========================
Structure of a botogram bot
===========================

botogram isn't just a library you can integrate with your code, but it's a
full framework which aims to help you creating bots, and to take full advantage
of that you need to follow some simple rules while creating your bot.

.. _bot-structure-skeleton:

A bot's skeleton
================

Even if you write two completly different bots, you'll have the same
boilerplate code in both of them. This is because you need to create the bot
instance, and start the runner after you executed all of your bot's code.

botogram tries to reduce the boilerplate code as much as possible, but some of
it is needed anyway. Here there is all the required code:

.. code-block:: python

   import botogram
   bot = botogram.create("YOUR-API-KEY")

   # Your code goes here

   if __name__ == "__main__":
       bot.run()

As you can see, there are two required code blocks in botogram:

* The first one imports botogram in your program, and creates a bot instance
  you can start to customize.

* The second one executes the bot. The if clausole is needed only if you plan
  to run your bot on Windows, so if you're using Linux or OSX you can omit it.

So, that's all the code required to create a bot with botogram. You can now
start the actual bot creation!

.. _bot-structure-hooks:

Introduction to hooks
=====================

Hooks are the way to go to add some logic to your bot: they allows you to react
when an user calls a command, write something or a lot more situations. Hooks
are added to your bot with decorated functions, or :ref:`with components
<custom-components>`.

For example, this is an hook which is executed when someone calls the ``/test``
command:

.. code-block:: python

   @bot.command("test")
   def test_command(chat, message, args):
       # Your hook's code

You can put any code you want in each hook, but remember hooks might be
executed in different processes by the runner, so avoid using global variables.
If you need to store global state check out :ref:`shared memory
<shared-memory>`.

.. _bot-structure-hooks-args:

Dynamic hooks arguments
=======================

Hooks are usually called with a lot of useful information, but you don't need
all of it every time. For example, you might not need shared memory in a whole
bot, but you have to use it everytime in another.

In order to avoid having to write everytime a really long list of arguments,
botogram is smart enought to figure out what you need and provide only that.
So, if in a command you just need the message and the shared memory, you can
define your hook this way:

.. code-block:: python

   @bot.command("test")
   def test_command(message, shared):
       # Your hook's code

In addition to the arguments provided by each hook, botogram allows you to
request those additional arguments:

* **bot**, which is an instance of the current bot.

* **shared**, which is an instance of your bot/component's :ref:`shared memory
  <shared-memory>`.
