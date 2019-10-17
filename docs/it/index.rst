.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _index:

======================
Documentazione - botogram
======================

*Just focus on your bots.*

botogram è un framework in python che ti consente di concentrarti
solo nella creazione del tuo `bot Telegram`_, senza preoccuparti della Bot API.

Mentre la maggior parte delle altre librerie fanno solo un wrapper della bot API,
botogram si concentra molto sull'esperienza di sviluppo, puntando a fornire la 
migliore API possibile. La maggior parte delle funzioni di Telegram sono gestite
da botogram, in modo tale che tu puoi concentrarti sul tuo bot. 

botogram è rilasciato sotto licenza MIT.

::

   import botogram
   bot = botogram.create("API-KEY")

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Saluta il mondo!"""
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()

.. _index-introduction:

Introduzione a botogram
========================

.. toctree::
   :maxdepth: 2

   install
   quickstart/index
   tricks

.. _index-narrative:

Documentazione narrativa
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

Referenze
=========

.. toctree::
   :maxdepth: 2

   api/index

.. _index-notes:

Informazioni utili
==========

.. toctree::
   :maxdepth: 2

   changelog/index
   license

.. _Telegram bots: https://core.telegram.org/bots
