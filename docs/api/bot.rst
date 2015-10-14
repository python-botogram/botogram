.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. api-bot::

~~~~~~~~~~~~~~~~~
Bots creation API
~~~~~~~~~~~~~~~~~

botogram is a microframework aimed to help you creating bots. It's obvious it
has something to create them! Here is the reference of all the needed
components.

.. py:function:: botogram.create(api_key)

   Create a new bot. This is a shortcut of directly creating the
   :py:class:`botogram.Bot` instance, because it automatically creates the API
   connection instance. Be sure to provide a valid API key.

   :param str api_key: The API key you received from Telegram
   :return: The bot instance
   :rtype: botogram.Bot

.. py:class:: botogram.Bot(api_connection)

   This class represents a single bot, and contains all of its logic. You can
   customize this class either extending it or with the decorators it provides.
   It requires a valid connection to the Telegram API.

   If you don't want to create the connection manually, it's better you use the
   :py:func:`botogram.create` utility function.

   :param botogram.TelegramAPI api_connection: The connection to the API

   .. py:attribute:: about

      About message of the bot, which should describe what the bot does. It
      will be displayed in the ``/help`` and ``/start`` builtin commands.

   .. py:attribute:: owner

      The username of the bot's owner, which will be displayed in the ``/help``
      command. This attribute will be sent directly to the user, so if you want
      to insert an username be sure to prefix it with ``@``, so the Telegram
      client will make that text clickable.

   .. py:attribute:: before_help

      A list of strings to be inserted in the ``/help`` messages. These ones
      will be inserted before the commands list.

   .. py:attribute:: after_help

      A list of strings to be inserted in the ``/help`` messages. These ones
      will be inserted after the commands list.

   .. py:attribute:: hide_commands

      A list of all the commands you want to hide from ``/help``. These
      commands won't be showed in the general ``/help``, but they will still be
      available for use or detailed help.

      This is useful if you want to keep some bot's commands private. It
      contains by default the ``/start`` command, and you shouldn't prepend the
      slash.

   .. py:attribute:: process_backlog

      A boolean representing if the backlog should be processed. Backlog is
      intended as all the messages sent to the bot before its startup. If
      this attribute is set to ``False``, as by default, the backlog is not
      processed by the bot.

   .. py:attribute:: itself

      The :py:class:`botogram.User` representation of the bot's user account.
      From this you can access its id, username and more.

   .. py:decoratormethod:: before_processing

      Functions decorated with this decorator will be called before an update
      is processed. This allows you, for example, to set up a filter on who can
      send messages to the bot. Decorated functions will be called with two
      parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

   .. py:decoratormethod:: process_message

      Functions decorated with this decorator will be called while processing
      an update. You can then do everything you want in it. Decorated functions
      will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

      .. note::

         This decorator is a low-level one: you might want to use the more
         friendly ones, like :py:meth:`botogram.Bot.message_contains`,
         :py:meth:`botogram.Bot.message_matches` and
         :py:meth:`botogram.Bot.command`.

   .. py:decoratormethod:: message_equals(string, [ignore_case=True])

      Functions decorated with this decorator will be called only if the
      processed message is equal to the ``string`` you provided. You may also
      define if you want to ignore the casing. Decorated functions will be
      called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter witht the representation of the received
        message (an instance of :py:class:`botogram.Message`).

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

      :param str string: The string you want equals to the message
      :param bool ignore_case: If the check should be ignore-case

   .. py:decoratormethod:: message_contains(string, [ignore_case=True, multiple=False])

      Functions decorated with this decorator will be called only if the
      processed message matches the ``string`` you provided. You may also
      define if you want to ignore the casing, and if the function should be
      called multiple times when multiple matches are found in the same
      message. Decorated functions will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

      :param str string: The string you want contained in the message
      :param bool ignore_case: If the match should be ignore-case
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:decoratormethod:: message_matches(regex, [flags=0, multiple=False])

      Functions decorated with this decorator will be called only if the
      processed message matches the ``regex`` you provided. You may also
      pass the ``re`` module's flags, and if the function should be called when
      multiple matches are found in the same message. Decorated functions will
      be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * A ``matches`` parameter with a tuple containing the matched groups

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

      :param str string: The string you want contained in the message
      :param int flags: ``re`` module's flags
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:decoratormethod:: command(name)

      This decorator register a new command, and calls the decorated function
      when someone issues the command in a chat. The command will also be added
      to the ``/help`` message. The decorated function will be called with
      three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * An ``args`` parameter with the list of parsed arguments

      If you put a docstring on the decorated function, that will be used as
      extended description of the command in the ``/help`` command.

      :param str name: The name of the command.

   .. py:decoratormethod:: init_shared_memory

      The function decorated with this decorator will be called the first time
      you access your bot's shared memory. This allows you to set the initial
      state of the memory, without having to put initialization code in every
      function which uses the shared memory. Please don't use this function as
      a "when the bot is started" hook, because it's not guaranteed to be
      called if you don't use shared memory.

      The decorated function will be called providing as first argument a
      dict-like object representing your bot's shared memory. Use it to
      initialize the things you want in the shared memory.

      .. code-block:: python

         @bot.init_shared_memory
         def initialize(shared):
             shared["messages"] = 0

         @bot.process_message
         @botogram.pass_shared
         def increment(shared, chat, message):
             if message.text is None:
                 return
             shared["messages"] += 1

         @bot.command("count")
         @botogram.pass_shared
         def count(shared, chat, message, args):
             chat.send("This bot received %s messages" % shared["messages"])

   .. py:method:: use(component)

      Use the provided component in your bot, so the hooks the component
      implements will be called while processing the updates. When you use
      another component, its hooks will be called before the one you provided
      before.

      :param botogram.Component component: The component you want to use.

   .. py:method:: process(update)

      Process a single update. This is useful if you want to manually process
      some updates or you want to create a custom runner.

      :param botogram.Update update: The update you want to process

   .. py:method:: run([workers=2])

      Run the bot with the multi-process runner botogram ships with. You can
      define how much update workers you want. Remember: the number of actual
      processes is the number you provide plus two (the current and the updates
      fetcher).

      Calls to this method are blocking, and the method won't return until the
      runner stops, so if you want to add other code to your bot, be sure to
      put it before the method call.

      :param int workers: The number of updates workers you want to use

   .. py:method:: freeze()

      Return a frozen instance of the bot. A frozen instance is exactly the
      same as the normal one, but you can't change the content of it. Frozen
      instances are used by the runner and by the
      :py:meth:`botogram.Bot.process` method.

      :return: A frozen instance of the current bot.
