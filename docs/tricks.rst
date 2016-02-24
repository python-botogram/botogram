.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _tricks:

~~~~~~~~~~~~~~~
Tips and tricks
~~~~~~~~~~~~~~~

The whole point of botogram is to make your life easier when creating Telegram
bots. In order to do so in a better way, there are some tricks you can use to
speed the development up.

.. _tricks-dynamic-arguments:

=================
Dynamic arguments
=================

There are a lot of information and methods you can get from every decorator,
but you don't always need them. botogram is smart enough to know which
arguments you want and in which order you want them. This means you can request
only the ones you need:

.. code-block:: python

   @botogram.command("test")
   def test(args, chat):
       chat.send(" ".join(args))

By default, the :py:meth:`~botogram.Bot.command` decorator provides three
arguments: ``chat``, ``message`` and ``args``. Instead, the function above
requested only two of them, and botogram is able to provide only them in the
right order.

Please remember this will work only if a function is called directly by
botogram (for example when a command is issued by an user). If you call it by
hand, you'll need to provide the arguments by hand.

There are some extra arguments you can request from every function called by
botogram, without being directly provided by the decorator:

* **bot**, which is an instance of the current bot.

* **shared**, which is an instance of the bot's
  :ref:`shared memory <shared-memory>`.

.. _tricks-messages-syntax:

=====================================
Rich formatting with message syntaxes
=====================================

Plain text messages can be boring for your users, and also hard to read if
those messages are full with information. Because of that, Telegram allows bots
to use rich formatting in their messages. Currently Telegram only supports `a
subset of`_ Markdown and HTML.

In order to use rich formatting in your messages you don't need to do anything:
botogram is smart enough to detect when a message uses rich formatting, and the
used syntax. If for whatever reason that detection fails, you can specify the
syntax you're using by providing it to the ``syntax`` parameter of the
:py:meth:`~botogram.Chat.send` method:

.. code-block:: python

   chat.send("*This is Markdown!*", syntax="markdown")

That parameter accepts the following values:

* ``markdown``, or its aliases ``md`` and ``Markdown``
* ``html``, or its alias ``HTML``

Also, if you don't want to use any rich formatting but the detector spots
something, you can disable it providing the special syntax ``plain`` to it:

.. code-block:: python

   chat.send("*I don't want this to be detected*", syntax="plain")

.. note::

   Support for rich formatting depends on your users' Telegram client. If
   they're using the official ones there are no problems, but that might work
   on unofficial clients.

.. _a subset of: https://core.telegram.org/bots/api#formatting-options
