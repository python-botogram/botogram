.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. api-utility::

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Utility functions and decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

botogram ships with some functions and decorators aimed to simplify the bots
development. Feel free to use them when you need them.


.. py:function:: botogram.usernames_in(message)

   Returns a list of usernames contained in the message you provide. The
   function automatically excludes commands, email addresses and URLs. Remember
   that returned usernames aren't prefixed with a ``@``.

   :param str message: The message which contains the usernames.
   :return: The list of usernames contained in the message.
   :rtype: list of str

.. py:decorator:: botogram.pass_bot

   Provide as first argument of the function the instance of the bot which
   called the function. This only works if the function is directly called from
   the bot, for example an hook called while processing an update.

   This can be useful if you need the bot instance but you can't access it.

.. py:decorator:: botogram.help_message_for(func)

   The return value of the decorated function will be treated as the help
   message of the function you pass to the decorator. The decorated function is
   called each time the help message is needed: this way you can create dynamic
   help messages, but it's advisable to cache the value if it's expensive to
   calculate it.

   :param callable func: The function which needs the help message.
