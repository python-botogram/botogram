.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _quickstart-skeleton:

================================
Creating the skeleton of the bot
================================

So, let's start with the actual creation of the bot. During this chapter, that
file will be called ``mybot.py``, so if you want to call the program in a
different way, remember to change all the references to it.

Open ``mybot.py`` with your favourite text editor, and insert this skeleton in
it:

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-API-KEY")

   if __name__ == "__main__":
       bot.run()

The first line imports the botogram microframework, allowing you to use it in
the program. The second one will create a brand new bot, with ``YOUR-API-KEY``
as the API key. Change that with the one you received in the previous step.
Finally, the third line will run the bot.

Even if right now the bot does nothing, you can run it by executing its file::

   $ python3 mybot.py

The bot will start running, and it will reply to each request you make to it.
In order to stop it, press ``Ctrl+C`` and, when it finishes processing the old
requests, it will close itself.
