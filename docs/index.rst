.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT licende

~~~~~~~~~~~~~~~~~~~~~~
botogram documentation
~~~~~~~~~~~~~~~~~~~~~~

*Just focus on your bots.*

botogram is a Python framework, which allows you to focus just on creating your
`Telegram bots`_, without worrying about the underlying Bots API.

While most of the libraries for Telegram out there just wrap the Bots API,
botogram focuses heavily on the development experience, aiming to provide you
the best API possible. Most of the Telegram implementation details are managed
by botogram, so you can just focus on your bot.

botogram is released under the MIT license.

::

   import botogram
   bot = botogram.create("YOUR-API-KEY")

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Say hello to the world!"""
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()

========================
Introduction to botogram
========================

.. toctree::
   :maxdepth: 2

   install
   tutorial/index
   channels
   tricks

===============
Advanced topics
===============

.. toctree::
   :maxdepth: 2

   shared-memory
   tasks
   custom-components
   deploy/index

=========
Reference
=========

.. toctree::
   :maxdepth: 2

   api/index

==========
Side notes
==========

.. toctree::
   :maxdepth: 2

   changelog
   license

.. _Telegram bots: https://core.telegram.org/bots
