.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _api-channels:

============
Channels API
============

The Channels API provides a lightweight way to interact with channels. If you
just want to send messages to a channel, it's better if you use this.


.. py:function:: botogram.channel(name, api_key)

   Create a new :py:class:`~botogram.Chat` object which points to the channel.
   You need to provide the channel name, prefixed with ``@``, and your bot's
   API key. Please refer to the :ref:`channels-preparation`
   section if you don't know how to get it.

   :param str name: The channel name.
   :param str api_key: Your bot's API key.
   :return: The corresponding Chat object.
   :rtype: botogram.Chat
