.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. api-bot::

=================
Bots creation API
=================

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
      to insert a username be sure to prefix it with ``@``, so the Telegram
      client will make that text clickable.

   .. py:attribute:: before_help

      A list of strings to be inserted in the ``/help`` messages. These ones
      will be inserted before the commands list.

   .. py:attribute:: after_help

      A list of strings to be inserted in the ``/help`` messages. These ones
      will be inserted after the commands list.

   .. py:attribute:: link_preview_in_help

      Disable link preview in the ``/help`` messages.

      .. versionadded:: 0.4

   .. py:attribute:: validate_callback_signatures

      Enable or disable signature verification for callbacks. Disabling them
      can cause security issues for your bot, and it's advised to do so only if
      you changed the bot token recently. See the :ref:`security section for
      callbacks <buttons-security>` for more details.

      The default value is **True**.

      .. versionadded:: 0.4

   .. py:attribute:: process_backlog

      A boolean representing if the backlog should be processed. Backlog is
      intended as all the messages sent to the bot before its startup. If
      this attribute is set to ``False``, as by default, the backlog is not
      processed by the bot.

   .. py:attribute:: itself

      The :py:class:`botogram.User` representation of the bot's user account.
      From this you can access its id, username and more.

   .. py:attribute:: lang

      The `ISO 639-1 code`_ assigned the language used by the bot.

   .. py:attribute:: override_i18n

      A dictionary that allows to override default i18n messages by associating
      the default ``msgid`` string of a message with its alternative.

      .. versionadded:: 0.5

   .. py:decoratormethod:: before_processing

      Functions decorated with this decorator will be called before an update
      is processed. This allows you, for example, to set up a filter on who can
      send messages to the bot. Decorated functions will be called with two
      parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

   .. py:decoratormethod:: process_message

      Functions decorated with this decorator will be called while processing
      an update. You can then do everything you want in it. Decorated functions
      will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
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
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
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
        message was sent (an instance of :py:class:`botogram.Chat`)
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
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * A ``matches`` parameter with a tuple containing the matched groups

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for this update.

      :param str string: The string you want contained in the message
      :param int flags: ``re`` module's flags
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:decoratormethod:: message_edited

      All the functions decorated with this method will be called when an user
      edits a message the bot knows about. This allows you, for example, to
      update the preview of a message if the user edits the request, or to
      enforce a no-edits policy on groups by banning whoever edits a message.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the decorated functions:

      * **chat**: the chat in which the message was originally sent (instance
        of :py:class:`~botogram.Chat`)

      * **message**: the edited message (instance of
        :py:class:`~botogram.Message`)

      .. code-block:: python

         @bot.message_edited
         def no_edits(chat, message):
             message.reply("You can't edit messages! Bye.")
             chat.ban(message.sender)

      .. versionadded:: 0.3

   .. py:decoratormethod:: channel_post

      Functions decorated with this decorator will receive all the messages
      posted to channels the bot is a member of. This allows you to act when
      certain messages are received, as an example.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the decorated functions:

      * **chat**: the chat in which the channel post was originally sent
        (instance of :py:class:`~botogram.Chat`)

      * **message**: the message (instance of :py:class:`~botogram.Message`)

      .. code-block:: python

         @bot.channel_post
         def channel_post(chat, message):
             message.reply("I read this post!")

      .. versionadded:: 0.4

   .. py:decoratormethod:: channel_post_edited

      Functions decorated with this decorator will receive all the messages
      edited in channels the bot is a member of. This allows you to act when
      certain messages are changed, as an example.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the decorated functions:

      * **chat**: the chat in which the channel post was originally sent
        (instance of :py:class:`~botogram.Chat`)

      * **message**: the (new) edited message (instance of
        :py:class:`~botogram.Message`)

      .. code-block:: python

         @bot.channel_post_edited
         def channel_post_edited(chat, message):
             message.reply("This post is changed!")

      .. versionadded:: 0.4

   .. py:decoratormethod:: command(name, [hidden=False, order=0])

      This decorator register a new command, and calls the decorated function
      when someone issues the command in a chat. The command will also be added
      to the ``/help`` message. The decorated function will be called with
      three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * An ``args`` parameter with the list of parsed arguments

      If you put a docstring on the decorated function, that will be used as
      extended description of the command in the ``/help`` command. Also, if
      you don't want this command to appear in the ``/help``, you can set the
      ``hidden`` argument to ``True``.

      :param str name: The name of the command.
      :param bool hidden: If the command should be hidden from ``/help``
      :param int order: The order in which the commands are shown in ``/help``

      .. versionchanged:: 0.4

         Added the ``order`` argument.

      .. versionchanged:: 0.3

         Added the ``hidden`` argument.

   .. py:decoratormethod:: callback(name)

      This decorator adds an handler for the callback with the provided name.
      See the chapter about :ref:`buttons and callbacks <buttons>` for more
      information about them.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the decorated function:

      * **query**: the received :py:class:`~botogram.CallbackQuery`

      * **chat**: the :py:class:`~botogram.Chat` from which the callback query
        was sent

      * **message**: the :py:class:`~botogram.Message` related to the callback
        query

      * **data**: the custom information provided by you along with the call

      .. code-block:: python

         @bot.command("greeter")
         def greeter_command(chat, message):
             """Say hi to the user"""
             btns = botogram.Buttons()
             btns[0].callback("Click me", "say-hi", message.sender.name)

             chat.send("Click the button below", attach=btns)

         @bot.callback("say-hi")
         def say_hi_callback(query, data):
             query.notify("Hi " + data)

      :param str name: the name of the callback

      .. versionadded:: 0.4

   .. py:decoratormethod:: chat_unavailable

      The decorated function is called when you try to send a message to a chat
      you can't send messages to. There are currently multiple reasons why that
      can happen, and you can see all of them :ref:`in the narrative
      documentation <unavailable-chats-reasons>`.

      The decorated function will be called with the following parameters:

      * **chat_id**: the ID of the chat which you can’t contact.
      * **reason**: the reason why you can’t contact the chat, as a string.

      If you want to learn more about unavailable chats check out :ref:`their
      documentation <unavailable-chats>`.

   .. py:decoratormethod:: timer(interval)

      Execute the decorated function periodically, at the provided interval,
      which must be in seconds. You can learn more in the :ref:`tasks-repeated`
      section of the docs.

      .. code-block:: python

         USER_ID = 12345

         @bot.timer(1)
         def spammer(bot):
             bot.chat(USER_ID).send("Hey!")

      :param int interval: The execution interval, in seconds.

   .. py:decoratormethod:: prepare_memory

      The function decorated with this decorator will be called the first time
      you access your bot's shared memory. This allows you to set the initial
      state of the memory, without having to put initialization code in every
      function which uses the shared memory. Please don't use this function as
      a "when the bot is started" hook, because it's not guaranteed to be
      called if you don't use shared memory.

      The decorated function will be called providing as first argument a
      dict-like object representing your bot's shared memory. Use it to
      prepare the things you want in the shared memory.

      .. code-block:: python

         @bot.prepare_memory
         def initialize(shared):
             shared["messages"] = 0

         @bot.process_message
         def increment(shared, chat, message):
             if message.text is None:
                 return
             shared["messages"] += 1

         @bot.command("count")
         def count(shared, chat, message, args):
             chat.send("This bot received %s messages" % shared["messages"])

      .. versionchanged:: 0.2

         Before it was called ``init_shared_memory``.

   .. py:decoratormethod:: init_shared_memory

      This decorator was renamed to
      :py:meth:`~botogram.Bot.prepare_memory` in botogram 0.2.
      Please use that instead of this.

      .. deprecated:: 0.2 it will be removed in botogram 1.0

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

   .. py:method:: edit_message(chat, message, text, [syntax=None, preview=True, extra=None])

      With this method you can edit the text of a message the user already
      received. This allows you to do a lot of interesting things, like
      live-updating information or showing paginated results: you just need to
      provide the id of the **message**, the id of the **chat** in which the
      message was sent, the new **text** of the message, and if you want to
      show the **preview**. The **syntax** parameter is for defining how the
      message text should be processed by Telegram (:ref:`learn more about rich
      formatting <tricks-messages-syntax>`).

      Please remember you can only edit messages your bot sent to the user.

      :param int chat: ID of the chat in which the message was sent
      :param int message: ID of the message you want to edit
      :param str text: The new text of the message
      :param bool preview: Whether to show link previews.
      :param str syntax: The name of the syntax used for the message.
      :param object extra: An extra reply interface object to attach.

      .. versionadded:: 0.3

   .. py:method:: edit_caption(caption, [extra=None])

      With this method you can edit the caption of the media attached to a
      message the user already received. This allows you to do a lot of
      interesting things, like live-updating information or showing dynamic
      subtitles: you just need to provide the new **caption**.

      Please remember you can only edit messages your bot sent to the user.

      :param str caption: The new caption of the media file.
      :param object extra: An extra reply interface object to attach.

      .. versionadded:: 0.3

   .. py:method:: chat(id)

      Get the :py:class:`~botogram.Chat` object of the chat with the ID you
      provided to this method. You can use this to get information about a chat
      you know about, or to send messages to other chats:

      .. code-block:: python

         BROADCAST_TO = [123, 321, 132]  # List of chat IDs

         @bot.command("broadcast")
         def broadcast_command(bot, chat, message, args):
             """Broadcast a message to multiple chats"""
             to_send = " ".join(args)

             for chat_id in BROADCAST_TO:
                 bot.chat(chat_id).send(to_send)

      If your bot can't access the chat, an exception will be raised. Check out
      the documentation about :ref:`unavailable chats <unavailable-chats>` to
      learn more about that.

      .. versionadded:: 0.3

      .. versionchanged:: 0.3.3

         If your bot can't access the chat, a ``ChatUnavailableError`` will be
         raised.

   .. py:method:: send(chat, message[, preview=True, reply_to=None, syntax=None, extra=None, notify=True])

      This method sends a message to a specific chat. The chat must be
      identified by its ID, and Telegram applies some restrictions on the chats
      allowed to receive your message: only users who sent you a message in the
      past are allowed, and also the group chats your bot is currently in.

      You must provide a message, and you can define if a preview for links
      should be showed (yes by default), the message ID of the message this one
      is replying to, and an extra object. One of these objects can be provided
      as the extra one:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *syntax* parameter is for defining how the message text should be
      processed by Telegram (:ref:`learn more about rich formatting
      <tricks-messages-syntax>`).

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the message.
      :param str message: The message you want to send.
      :param bool preview: If you want to show the link preview.
      :param int reply_to: The ID of the message this one is replying to.
      :param string syntax: The name of the syntax you used for the message.
      :param object extra: An extra object you want to attach (see above).
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_photo(chat, path[, caption="", reply_to=None, extra=None, notify=True])

      This method sends a photo to a specific chat. The chat must be identified
      by its ID, and Telegram applies some restrictions on the chats allowed to
      receive your photo: only users who sent you a message in the past are
      allowed, and also the group chats your bot is currently in.

      You must provide the path to the photo, and you can specify a photo
      caption, the message ID of the message this one is replying to, and an
      extra object. One of these objects can be provided as the extra one:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the photo.
      :param str path: The path to the photo you want to send.
      :param str caption: An optional caption for the photo.
      :param int reply_to: The ID of the message this one is replying to.
      :param object extra: An extra object you want to attach (see above).
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_audio(chat, path, [duration=None, performer=None, title=None, reply_to=None, extra=None, notify=True])

      This method sends an audio track to a specific chat. The chat must be
      identified by its ID, and Telegram applies some restrictions on the chats
      allowed to receive your photo: only users who sent you a message in the
      past are allowed, and also the group chats your bot is currently in.

      You must provide the *path* to the audio track, and you may optionally
      specify the *duration*, the *performer* and the *title* of the audio
      track. If the audio track you're sending is in reply to another message,
      set *reply_to* to the ID of the other :py:class:`~botogram.Message`.
      *extra* is an optional object which specifies additional reply interface
      options on the recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the photo.
      :param str path: The path to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_voice(chat, path, [duration=None, reply_to=None, extra=None, notify=True])

      This method sends a voice message to a specific chat. The chat must be
      identified by its ID, and Telegram applies some restrictions on the chats
      allowed to receive your photo: only users who sent you a message in the
      past are allowed, and also the group chats your bot is currently in.

      You must provide the *path* to the voice message, and you may optionally
      specify the *duration* of the voice message. If the voice message you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the photo.
      :param str path: The path to the voice message
      :param int duration: The message duration, in seconds
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_video(chat, path, [duration=None, caption=None, reply_to=None, extra=None, notify=True])

      This method sends a video to a specific chat. The chat must be identified
      by its ID, and Telegram applies some restrictions on the chats allowed to
      receive your photo: only users who sent you a message in the past are
      allowed, and also the group chats your bot is currently in.

      You must provide the *path* to the video, and you may optionally specify
      the *duration* and the *caption* of the video. If the video you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the video
      :param str path: The path to the video
      :param int duration: The video duration, in seconds
      :param str caption The caption of the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_file(chat, path, [reply_to=None, extra=None, notify=True])

      This method sends a generic file to a specific chat. The chat must be
      identified by its ID, and Telegram applies some restrictions on the chats
      allowed to receive your photo: only users who sent you a message in the
      past are allowed, and also the group chats your bot is currently in.

      You must provide the *path* to the file. If the file you're sending is in
      reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the file
      :param str path: The path to the file
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_location(chat, latitude, longitude, [reply_to=None, extra=None, notify=True])

      This method sends a geographic location to a specific chat. The chat must
      be identified by its ID, and Telegram applies some restrictions on the
      chats allowed to receive your locations: only users who sent you a
      message in the past are allowed, and also the group chats your bot is
      currently in.

      If the location you're sending is in reply to another message, set
      *reply_to* to the ID of the other :py:class:`~botogram.Message`.  *extra*
      is an optional object which specifies additional reply interface options
      on the recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the location
      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:method:: send_sticker(sticker, [reply_to=None, extra=None, notify=True])

      This method sends a sticker to a specific chat chat (in webp format). The
      chat must be identified by its ID, and Telegram applies some restrictions
      on the chats allowed to receive your locations: only users who sent you a
      message in the past are allowed, and also the group chats your bot is
      currently in.

      If the sticker you're sending is in reply to another message, set
      *reply_to* to the ID of the other :py:class:`~botogram.Message`. *extra*
      is an optional object which specifies additional reply interface options
      on the recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int chat: The ID of the chat which should receive the location
      :param str sticker: The path to the webp-formatted sticker
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. deprecated:: 0.3 it will be removed in botogram 1.0

   .. py:attribute:: hide_commands

      This attribute is now deprecated, use the ``hidden`` argument of the
      method you use to register commands (for example the
      :py:meth:`~botogram.Bot.command` decorator or the
      :py:meth:`~botogram.Component.add_command` method of your component).

      A list of all the commands you want to hide from ``/help``. These
      commands won't be showed in the general ``/help``, but they will still be
      available for use or detailed help.

      .. deprecated:: 0.3 it will be removed in botogram 1.0

.. _`ISO 639-1 code`: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes