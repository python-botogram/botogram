.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _tricks:

===============
Tips and tricks
===============

The whole point of botogram is to make your life easier when creating Telegram
bots. In order to do so in a better way, there are some tricks you can use to
speed the development up.

.. _tricks-messages-syntax:

Rich formatting with message syntaxes
=====================================

Plain text messages can be boring for your users, and also hard to read if
those messages are full with information. Because of that, Telegram allows bots
to use rich formatting in their messages. Currently Telegram only supports `a
subset of`_ Markdown and HTML.

In order to use rich formatting in your messages you don't need to do anything:
botogram is smart enough to detect when a message uses rich formatting as well
as which syntax is used. If for whatever reason that detection fails, you can
specify the syntax you're using by providing it to the ``syntax`` parameter of
the :py:meth:`~botogram.Chat.send` method:

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

   Support for rich formatting depends on your users' Telegram client. All
   official clients are supported, where unofficial clients may not support
   all or any rich formatting syntax.

.. _a subset of: https://core.telegram.org/bots/api#formatting-options
