.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _index:

======================
botogram documentation
======================

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

.. _index-introduction:

Introduction to botogram
========================

.. toctree::
   :maxdepth: 2

   install
   quickstart/index
   tricks

.. _index-narrative:

Narrative documentation
=======================

.. toctree::
   :maxdepth: 2

   bot-creation
   bot-structure
   unavailable-chats
   groups-management
   buttons
   shared-memory
   tasks
   custom-components
   deploy/index
   channels
   i18n

.. _index-reference:

Reference
=========

.. toctree::
   :maxdepth: 2

   api/index

.. _index-notes:

Side notes
==========

.. toctree::
   :maxdepth: 2

   changelog/index
   license

.. _Telegram bots: https://core.telegram.org/bots
