.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. api-utility::

================================
Utility functions and decorators
================================

botogram ships with some functions and decorators aimed to simplify the bots
development. Feel free to use them when you need them.


.. py:function:: botogram.run(*bots[, workers=2])

   This function allows you to run multiple bots in the same runner. You just
   need to provide all the bots you want to run, and the options you would
   normally provide to the bot's run method.

   Remember this function is blocking, so it prevents the execution of the code
   after the call until the runner is closed. Use a thread or a process if you
   want to execute things other than just running the runner.

   .. code-block:: python

      import botogram
      from file1 import bot as bot1
      from file2 import bot as bot2

      if __name__ == "__main__":
          botogram.run(bot1, bot2)

   :param botogram.Bot \*bots: The bots you want to run.
   :param int workers: The number of workers you want to use.

.. py:function:: botogram.usernames_in(message)

   Returns a list of usernames contained in the message you provide. The
   function automatically excludes commands, email addresses and URLs. Remember
   that returned usernames aren't prefixed with a ``@``.

   :param str message: The message which contains the usernames.
   :return: The list of usernames contained in the message.
   :rtype: list of str


.. py:decorator:: botogram.pass_shared

   This decorator does nothing currently. If you still use it, just remove all
   the references to it in your source code. Your bot will still work
   flawlessly.

   .. deprecated:: pre-0.1 it will be removed in botogram 1.0

.. py:decorator:: botogram.pass_bot

   This decorator does nothing currently. If you still use it, just remove all
   the references to it in your source code. Your bot will still work
   flawlessly.

   .. deprecated:: pre-0.1 it will be removed in botogram 1.0

.. py:decorator:: botogram.help_message_for(func)

   The return value of the decorated function will be treated as the help
   message of the function you pass to the decorator. The decorated function is
   called each time the help message is needed: this way you can create dynamic
   help messages, but it's advisable to cache the value if it's expensive to
   calculate it.

   :param callable func: The function which needs the help message.


.. _picklable objects: https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled
