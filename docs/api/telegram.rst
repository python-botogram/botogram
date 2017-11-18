.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _api-telegram:

====================
Telegram API wrapper
====================

As an advantage to using botogram's :ref:`higher level API<api-bot>` and bot
runner, many distracting and tedious details of working with
`Telegram's Bot API`_ are hidden away. Furthermore you gain many great
conveniences. It is generally unnecessary to know anything about Telegram's own
`API methods`_, which have either been nicely abstracted away or concisely
integrated into the classes presented here. These classes wrap Telegram's
`API types`_ and detail the core objects your bot will deal with when going
about its business.

* :py:class:`~botogram.User`
* :py:class:`~botogram.Chat`
* :py:class:`~botogram.Message`
* :py:class:`~botogram.Photo`
* :py:class:`~botogram.PhotoSize`
* :py:class:`~botogram.Audio`
* :py:class:`~botogram.Document`
* :py:class:`~botogram.Sticker`
* :py:class:`~botogram.Video`
* :py:class:`~botogram.Voice`
* :py:class:`~botogram.Contact`
* :py:class:`~botogram.Location`
* :py:class:`~botogram.Venue`
* :py:class:`~botogram.Update`
* :py:class:`~botogram.UserProfilePhotos`
* :py:class:`~botogram.ReplyKeyboardMarkup`
* :py:class:`~botogram.ReplyKeyboardHide`
* :py:class:`~botogram.ForceReply`


.. py:class:: botogram.User

   This class represents a Telegram user.

   .. py:attribute:: id

      The integer ID of the user.

   .. py:attribute:: first_name

      The first name of the user.

   .. py:attribute:: last_name

      The last name of the user.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: username

      The user's username, without the ``@`` prefix.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: name

      The computed name of the user. If someone has only the first name, this
      attribute contains it, but if someone also has a last name, this
      attribute contains the two merged.

      You can't write to this attribute, but it automatically updates when you
      change :py:attr:`~botogram.User.first_name` or
      :py:attr:`~botogram.User.last_name`.

      .. versionadded:: 0.2

   .. py:attribute:: avatar

      This attribute contains the user's avatar, represented as a
      :py:class:`~botogram.Photo` object. If the user has no avatar, this
      attribute will be ``None``.

      In order to improve performances, this attribute's content is dynamically
      requested to Telegram the first time you access it, so there will be some
      delay.

      .. versionadded:: 0.2

   .. py:method:: avatar_history()

      Get the user's avatar history. This returns a list of the current and all
      the past avatars for the user, represented as :py:class:`~botogram.Photo`
      objects. If the user has no avatars this returns an empty list.

      .. versionadded:: 0.2

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, attach=None, extra=None, notify=True])

      Send the textual *message* to the user. You may optionally stop clients
      from generating a *preview* for any link included in the message. If the
      message you are sending is in reply to another, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`. The *syntax* parameter is for
      defining how the message text should be processed by Telegram
      (:ref:`learn more about rich formatting <tricks-messages-syntax>`).

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to be sent.
      :param bool preview: Whether to show link previews.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param str syntax: The name of the syntax used for the message.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_photo([path=None, file_id=None, url=None, caption=None, reply_to=None, extra=None, attach=None, notify=True])

      Send a photo to the user. You can specify the photo by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify a *caption* for the photo being sent.
      If the photo you are sending is in reply to another message,
      set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str file_id: The Telegram *file_id* of the photo.
      :param str url: The URL to the photo.
      :param str caption: A caption for the photo.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message
         
      .. versionchanged:: 0.5

         Added support for *file_id* and *url*.

   .. py:method:: send_audio([path=None, file_id=None, url=None, duration=None, performer=None, title=None, reply_to=None, attach=None, extra=None, notify=True, caption=None])

      Send an audio track to the user. You can specify the track by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify the *duration*, the *performer* and the *title* 
      of the audio track. If the audio track you're sending is in reply to another message,
      set *reply_to* to the ID of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the audio track
      :param str file_id: The Telegram *file_id* of the audio track
      :param str url: The URL to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the audio track.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message
         
      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*.

   .. py:method:: send_voice([path=None, file_id=None, url=None, duration=None, reply_to=None,  extra=None, attach=None, notify=True, caption=None])

      Send a voice message to the user. You can specify the audio by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify the *duration* of the voice message. If the voice
      message you're sending is in reply to another message, set *reply_to* to
      the ID of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param str file_id: The Telegram *file_id* of the voice message
      :param str url: The URL to the audio
      :param int duration: The message duration, in seconds
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the voice message.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message
         
      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*.

   .. py:method:: send_video([path=None, file_id=None, url=None, duration=None, caption=None, reply_to=None, attach=None, extra=None, notify=True])

      Send a video to the user. You can specify the video by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify the *duration* and the *caption* of the video.
      If the audio track you're sending is in reply to another message, 
      set *reply_to* to the ID of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param str file_id: The Telegram *file_id* of the video
      :param str url: The URL to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message
         
       .. versionchanged:: 0.5

         Added support for *file_id* and *url*.

   .. py:method:: send_file([path=None, file_id=None, url=None, reply_to=None, attach=None, extra=None, notify=True, caption=None])

      Send a generic file to the user. You can specify the file by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      If the file you're sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param str file_id: The Telegram *file_id* of the video
      :param str url: The URL to the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the file.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message
         
      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*.

   .. py:method:: send_location(latitude, longitude, [reply_to=None, attach=None, extra=None, notify=True])

      Send the geographic location to the user. If the location you're sending
      is in reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_venue(latitude, longitude, title, address, [foursquare=None, reply_to=None, attach=None, extra=None, notify=True])

      Send a venue to the user. A venue is made of its geographic coordinates
      (latitude and longitude), its title and address, and optionally the
      venue's Foursquare ID, if you want to integrate with that. Users will
      then see the venue in the map, along with the information you provided.

      You can use this, for example, if you want to recommend to your bot's
      users a place to go to dinner tonight:

      .. code-block:: python

         @bot.command("whereshouldigo")
         def whereshouldigo_command(chat, message, args):
             message.sender.send("Here there is an unique place to go to dinner tonight!")
             message.sender.send_venue(35, -45, "The Abyss", "Atlantic Ocean")

      The *attach* parameter also allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param float latitude: The latitude of the venue
      :param float longitude: The longitude of the venue
      :param str title: The name of the venue
      :param str address: The address of the venue
      :param str foursquare: The Foursquare ID of the venue
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: send_sticker(sticker, [reply_to=None, attach=None, extra=None, notify=True])

      Send the sticker to the user (in webp format). If the sticker you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_contact(phone, first_name, [last_name=None, reply_to=None, attach=None, extra=None, notify=True])

      Send a contact to the user. A Telegram contact is made of its phone
      number (with the international prefix), its first name and optionally its
      last name. You can use this, for example, to send the user the phone
      number of a buisness so he can call them:

      .. code-block:: python

         @bot.command("support")
         def support_command(chat, message, args):
             message.sender.send("Hi there, here is our support number:")
             message.sender.send_contact("+390124567890", "Support")

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      :param str phone: The phone number of the contact
      :param str first_name: The first name of the contact
      :param str last_name: The last name of the contact
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: delete_message(message)

      Delete the message with the provided ID or :py:class:`~botogram.Message` object.
      A message can be deleted only if is sent by the bot or sent in a supergroup by an user where the bot is admin.
      It can also be deleted if it's one of the supported service messages.

      :param message: The message to delete (can be an ID too)

      .. versionadded:: 0.4

.. py:class:: botogram.Chat

   This class represents a Telegram chat.

   .. py:attribute:: id

      The integer ID of the chat.

   .. py:attribute:: type

      The type of chat, either ``private``, ``group``, ``supergroup`` or ``channel``.

   .. py:attribute:: title

      A title specified for group chats and channels.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: username

      The username of the user opposite the bot in a private chat or owner of
      the channel.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: first_name

      The first name of the user opposite the bot in a private chat or owner of
      the channel.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: last_name

      The last name of the user opposite the bot in a private chat or owner of
      the channel.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: name

      The computed name of the chat. If this chat has a title this attribute
      contains it. If someone has only the first name, this attribute contains
      it, but if someone also has a last name, this attribute contains the two
      merged.

      You can't write to this attribute, but it automatically updates when you
      change :py:attr:`~botogram.Chat.title`,
      :py:attr:`~botogram.Chat.first_name` or
      :py:attr:`~botogram.Chat.last_name`.

      .. versionadded:: 0.2

   .. py:attribute:: admins

      The list of the administrators of the group (or supergroup), represented
      as a list of :py:class:`~botogram.User`. If the chat is a private chat, a
      list containing only the chat partner is returned. Instead, a
      ``TypeError`` is raised if the chat is a channel.

      Please remember the content of this attribute is fetched from Telegram
      the first time you access it (so it might be slow), but it's cached right
      after, so the following accesses will involve no network communication.

      .. code-block:: python
         :emphasize-lines: 14,15,16

         # This hook bans a member of the group if an admin replies to one of
         # its messages with "#ban"

         @bot.process_message
         def ban_users(chat, message):
            # Allow only groups
            if message.type not in ("group", "supergroup"):
                return

            # Allow only replies with text in the reply
            if message.text is None or message.reply_to_message is None:
                return

            # Allow only admins to ban people
            if message.sender not in chat.admins:
                return

            # Match the text and ban the original message sender
            if message.text == "#ban":
                chat.ban(message.reply_to_message.sender)

      .. versionadded:: 0.3

   .. py:attribute:: creator

      Return the creator of the group (or supergroup), represented as an
      :py:class:`~botogram.User`. If the chat is a private chat, the chat
      partner is returned. Instead, a ``TypeError`` is raised if the chat is a
      channel.

      Please remember the content of this attribute is fetched from Telegram
      the first time you access it (so it might be slow), but it's cached right
      after, so the following accesses will involve no network communication.

      .. code-block:: python
         :emphasize-lines: 4,5,6

         @bot.command("antiflood_limit")
         def antiflood_limit_command(shared, chat, message, args):
             """Set the antiflood limit"""
             # Only the chat creator should be able to do this
             if message.sender != chat.creator:
                 message.reply("You're not the creator of the chat")

             if len(args) != 1:
                 message.reply("You need to provide just the new limit!")
             shared["antiflood_limit"] = int(args[0])

      .. versionadded:: 0.3

   .. py:attribute:: members_count

      Return the number of members of this chat. This works across all the
      kinds of chat.

      Please remember the content of this attribute is fetched from Telegram
      the first time you access it (so it might be slow), but it's cached right
      after, so the following accesses will involve no network communication.

      .. code-block:: python

         @bot.command("members")
         def members_command(chat, message, args):
             """Get the number of members in this group"""
             chat.send(str(chat.members_count))

      .. versionadded:: 0.3

   .. py:method:: status_of(user)

      Return the status of the provided user (either an instance of
      :py:class:`~botogram.User` or an ID) in the group chat. A ``TypeError``
      is raised if the current chat is a private conversation or a channel.

      Currently available statuses:

      * **creator**: this user created the group in the first place
      * **administrator**: the user is an admin appointed by the group creator
      * **member**: the user is a normal member of the group
      * **left**: the user left the group in the past or never joined it
      * **kicked**: the user was kicked by an administrator out of the group

      Please remember the content of this attribute is fetched from Telegram
      the first time you access it (so it might be slow), but it's cached right
      after, so the following accesses will involve no network communication.

      .. code-block:: python
         :emphasize-lines: 6,7

         @bot.command("status_of")
         def status_of_command(chat, message, args):
             if len(args) != 1:
                 message.reply("You must provide just the ID of the user!")

             status = chat.status_of(int(args[0]))
             chat.send("*%s*" % status)

      :param user: the user you want to check the status of (either
                   :py:class:`~botogram.User` or the user ID as an ``int``)
      :returns: the status of the user
      :rtype: str

      .. versionadded:: 0.3

   .. py:method:: leave()

      Kick the bot from this chat. This method is available only on groups and
      supergroups, and the bot must be a member of the chat.

      This method might be handy if the other members of the group are abusing
      your bot, or spamming it with too much messages. Keep in mind though, an
      admin of the chat can re-add your bot at any time, so if you want to
      forget about it you need to store the chat ID somewhere and leave the
      group as soon as your bot joins it.

      .. code-block:: python

         @bot.command("bye")
         def bye_command(chat):
             chat.leave()

      .. versionadded:: 0.3

   .. py:method:: ban(user)

      Ban the provided user from this group chat. You can either provide the
      user ID or an instance of :py:class:`~botogram.User`. This method is the
      cornerstone of :ref:`moderating group chats <manage-chats>`, since it
      allows your bot to punish misbehaving users.

      While on normal group chats a banned user can rejoin the chat if it's
      added by one of its members or he uses a join link, on supergroups you
      need to explicitly :py:meth:`~botogram.Chat.unban` he to let him rejoin.

      Remember your bot must be an administrator of the chat in order to this
      method to work properly.

      .. code-block:: python

         # This command bans the user who sent the message you replied to

         @bot.command("ban")
         def ban_user(chat, message, args):
             """Ban that user"""
             # Some needed filtering and error handling
             if message.reply_to_message is None:
                 message.reply("You must reply to a message the user wrote!")
             if message.sender not in chat.admins:
                 message.reply("You must be an admin of the group!")
             if message.reply_to_message.sender in chat.admins:
                 message.reply("You can't ban another admin!")

             chat.ban(message.reply_to_message.sender)

      :param int user: The user you want to ban (user ID or
                       :py:class:`~botogram.User`)

      .. versionadded:: 0.3

   .. py:method:: unban(user)

      Unban the user from this group chat. This does nothing on normal group
      chats, but it removes the user from the group's blacklist if the chat is
      a supergroup. This method can be handy if you want to remove the ban you
      given to an user.

      Remember your bot must be an administrator of the chat in order to this
      method to work properly.

      .. code-block:: python

         @bot.timer(60)
         def unban_all(shared, bot):
             # This unbans all the users in the shared memory
             for chat_id, user_id in shared["banned_users"].items():
                 bot.chat(chat_id).unban(user_id)

             shared["banned_users"] = {}

      :param int user: The user you want to unban (user ID or
                       :py:class:`~botogram.User`)

      .. versionadded:: 0.3

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, attach=None, extra=None, notify=True])

      Send the textual *message* to the chat. You may optionally stop clients
      from generating a *preview* for any link included in the message. If the
      message you are sending is in reply to another, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`. The *syntax* parameter is for
      defining how the message text should be processed by Telegram
      (:ref:`learn more about rich formatting <tricks-messages-syntax>`).

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to be sent.
      :param bool preview: Whether to show link previews.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param str syntax: The name of the syntax used for the message.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_photo([path=None, file_id=None, url=None, caption=None, reply_to=None, attach=None, extra=None, attach=None, notify=True])

      Send a photo to the chat. You can specify the photo by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify a
      *caption* for the photo being sent. If the photo you are sending is in
      reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str file_id: The Telegram *file_id* of the photo.
      :param str url: The URL to the photo.
      :param str caption: A caption for the photo.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. versionchanged:: 0.5

         Added support for *file_id* and *url*

   .. py:method:: send_audio([path=None, file_id=None, url=None, duration=None, performer=None, title=None, reply_to=None, extra=None, attach=None, notify=True, caption=None])

      Send an audio track to the chat. You can specify the track by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally
      specify the *duration*, the *performer* and the *title* of the audio
      track. If the audio track you're sending is in reply to another message,
      set *reply_to* to the ID of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the audio track
      :param str file_id: The Telegram *file_id* of the track
      :param str url: The URL to the track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the audio track.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*

   .. py:method:: send_voice([path=None, file_id=None, url=None, duration=None, reply_to=None, extra=None, attach=None, notify=True, caption=None])

      Send a voice message to the chat. You can specify the audio by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally specify the *duration* of the voice message. If the voice
      message you're sending is in reply to another message, set *reply_to* to
      the ID of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param str file_id: The Telegram *file_id* of the audio
      :param str url: The URL to the audio
      :param int duration: The message duration, in seconds
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the voice message.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*

   .. py:method:: send_video([path=None, file_id=None, url=None, duration=None, caption=None, reply_to=None, extra=None, attach=None, notify=True])

      Send a video to the chat. You can specify the video by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      You may optionally
      specify the *duration* and the *caption* of the video. If the audio track
      you're sending is in reply to another message, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param str file_id: The Telegram *file_id* of the video
      :param str url: The URL to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. versionchanged:: 0.5

         Added support for *file_id* and *url*

   .. py:method:: send_file([path=None, file_id=None, url=None, reply_to=None, attach=None, extra=None, notify=True, caption=None])

      Send a generic file to the chat. You can specify the video by passing its *path*,
      its *url*, or its Telegram *file_id*. Only one of these arguments must be passed.
      
      If the file you're sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param str file_id: The Telegram *file_id* of the file
      :param str url: The URL to the file
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :param str caption: A caption for the file.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

      .. versionchanged:: 0.5

         Added support for *caption*, *file_id* and *url*

   .. py:method:: send_location(latitude, longitude, [reply_to=None, attach=None, extra=None, notify=True])

      Send the geographic location to the chat. If the location you're sending
      is in reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_venue(latitude, longitude, title, address, [foursquare=None, reply_to=None, attach=None, extra=None, notify=True])

      Send a venue to the chat. A venue is made of its geographic coordinates
      (latitude and longitude), its title and address, and optionally the
      venue's Foursquare ID, if you want to integrate with that. Users will
      then see the venue in the map, along with the information you provided.

      You can use this, for example, if you want to recommend to your bot's
      users a place to go to dinner tonight:

      .. code-block:: python

         @bot.command("whereshouldigo")
         def whereshouldigo_command(chat, message, args):
             chat.send("Here there is an unique place to go to dinner tonight!")
             chat.send_venue(35, -45, "The Abyss", "Atlantic Ocean")

      :param float latitude: The latitude of the venue
      :param float longitude: The longitude of the venue
      :param str title: The name of the venue
      :param str address: The address of the venue
      :param str foursquare: The Foursquare ID of the venue
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: send_sticker(sticker, [reply_to=None, attach=None, extra=None, notify=True])

      Send the sticker to the chat (in webp format). If the sticker you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: send_contact(phone, first_name, [last_name=None, reply_to=None, attach=None, extra=None, notify=True])

      Send a contact to the chat. A Telegram contact is made of its phone
      number (with the international prefix), its first name and optionally its
      last name. You can use this, for example, to send the user the phone
      number of a buisness so he can call them:

      .. code-block:: python

         @bot.command("support")
         def support_command(chat, message, args):
             chat.send("Hi there, here is our support number:")
             chat.send_contact("+390124567890", "Support")

      :param str phone: The phone number of the contact
      :param str first_name: The first name of the contact
      :param str last_name: The last name of the contact
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: delete_message(message)

      Delete the message with the provided ID or :py:class:`~botogram.Message` object.
      A message can be deleted only if is sent by the bot or sent in a supergroup by an user where the bot is admin.
      It can also be deleted if it's one of the supported service messages.

      :param message: The message to delete (can be an ID too)

      .. versionadded:: 0.4

.. py:class:: botogram.ParsedText

   This class contains the parsed representation of the text of a received
   message. This allows you to work with the rich-formatted text the user sent,
   in addition to the plaintext provided by the :py:class:`~botogram.Message`
   class.

   This class behaves as a list of :py:class:`~botogram.ParsedTextEntity`, so
   you can access its items as you would do with any other list (indexed
   access, iteration...), but it also provides some other utility tools.

   .. versionadded:: 0.3

   .. describe:: type in parsed

      Check if a given entity type is contained in the message. For example,
      with the following code you can check if the user sent links in his
      message:

      .. code-block:: python

         if "url" in message.parsed_text:
             chat.send("Hey, you sent me a link!")

   .. py:method:: filter(\*types, [exclude=False])

      This method returns a list of all the
      :py:class:`~botogram.ParsedTextEntity` in a message of a given
      type. This allows you to get only some types of entities, and exclude the
      other ones in a simple way. You can also just **exclude** from the result
      the types you provide.

      .. code-block:: python

         # Get only the URLs
         urls = message.parsed_text.filter("url")

         # Get usernames and hashtags
         usernames_hashtags = message.parsed_text.filter("mention", "hashtag")

         # Exclude plaintext
         entities = message.parsed_text.filter("plaintext", exclude=True)

.. py:class:: botogram.ParsedTextEntity

   This class represent a single entity contained in a text message.

   .. versionadded:: 0.3

   .. describe:: str(entity)

      An handy alias for the :py:attr:`~botogram.ParsedTextEntity.text`
      attribute.

   .. describe:: len(entity)

      Return the length of the entity.

   .. py:attribute:: type

      The type of the entity. This can be one of those:

      * **plain**: a plain string (with no formatting or special meaning)

      * **mention**: a mention to another user (can contain the username or the
        full name, for example ``@pietroalbini`` or ``Pietro``)

      * **hashtag**: an hashtag (for example ``#pythonftw``)

      * **command**: a command sent to a bot (for example ``/help``)

      * **link** a link (the text can contain its label)

      * **email**: an email address (for example ``pietro@pietroalbini.io``)

      * **bold**: a bold-formatted text

      * **italic**: an italic-formatted text

      * **code**: a monospace-formatted text

      * **pre**: a monospace-formatted block

   .. py:attribute:: text

      Return the plaintext content of the entity. In pair with the type you can
      recreate the original formatting of the entity.

   .. py:attribute:: url

      The attached URL for the entity. This includes the raw URL for the
      **url** type, the ``telegram.me`` link for the **mention** type (if the
      user has an username), and the ``mailto:`` link for **email** type.

   .. py:attribute:: user

      The :py:class:`~botogram.User` mentioned in this entity. This isn't
      always provided by Telegram, currently only if the mentioned user doesn't
      have an username.

.. py:class:: botogram.Message

   This class represents messages received by and sent from your bot. Messages
   serve as a container for many of the core API objects described here.

   .. py:attribute:: message_id

      The integer ID of the message.

   .. py:attribute:: sender

      The sending :py:class:`~botogram.User` of the message. Note the trailing
      underscore, needed due to 'from' being a python keyword.

      *This attribute can be None if it's not provided by Telegram.*

      .. versionchanged:: 0.2 Before it was called ``from_``.

   .. py:attribute:: from_

      The sending :py:class:`~botogram.User` of the message. Note the trailing
      underscore, needed due to 'from' being a python keyword.

      *This attribute can be None if it's not provided by Telegram.*

      .. deprecated:: 0.2 It will be removed in botogram 1.0

   .. py:attribute:: date

      The integer date of when the message was sent, in Unix time.

   .. py:attribute:: chat

      The :py:class:`~botogram.Chat` to which the message belongs.

   .. py:attribute:: forward_from

      The sender of the original message, if this message was forwarded. This
      attribute can contain one of the following objects:

      * :py:class:`~botogram.User` when the original sender is an user
      * :py:class:`~botogram.Chat` when the message originated in a channel

      *This attribute can be None if it's not provided by Telegram.*

      .. versionchanged:: 0.3

         The value can also be an instance of :py:class:`~botogram.Chat`.

   .. py:attribute:: forward_from_message_id

      The ID of the original message that was forwarded. This is currently only
      available for channel posts.

      .. versionadded:: 0.4

   .. py:attribute:: forward_date

      The integer date (in Unix time) of when the original message was sent,
      when this message is a forward.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: reply_to_message

      The :py:class:`~botogram.Message` for which *this* message is a reply to.
      Note that the message returned by this attribute will not contain further
      *reply_to_message* objects, even if it is itself a reply.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: text

      The UTF-8 text for when this message is a text message.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: parsed_text

      The :py:class:`~botogram.ParsedText` representation of the text of this
      message.

      *This attribute is None if the text attribute is also None.*

      .. versionaddedd: 0.3

   .. py:attribute:: audio

      An :py:class:`~botogram.Audio` object, for when this message is an audio
      file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: voice

      A :py:class:`~botogram.Voice` object, for when this message is a voice
      file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: document

      A :py:class:`~botogram.Document` object, for when this message is a
      general file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: photo

      A :py:class:`~botogram.Photo` object, for when this message is a photo
      file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: sticker

      A :py:class:`~botogram.Sticker` object, for when this message is a sticker
      file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: video

      A :py:class:`~botogram.Video` object, for when this message is a video
      file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: caption

      A caption for when this message is a photo or video file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: contact

      A :py:class:`~botogram.Contact` object, for when this message is a shared
      contact.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: location

      A :py:class:`~botogram.Location` object, for when this message is a shared
      location.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: venue

      If the user sent a :py:class:`~botogram.Venue` with this message, the
      attribute contains its representation.

      *This attribute can be None if the message isn't a venue.*

   .. py:attribute:: channel_post_author

      The author of the message. This only works if the message is a channel
      post and it's signed by the author, even if the message is forwarded.
      Otherwise it's *None*.

      .. versionadded:: 0.4

   .. py:attribute:: new_chat_member

      A :py:class:`~botogram.User` object representing a new member of a group
      chat. This user may be a bot.

      *This attribute can be None if it's not provided by Telegram.*

      .. versionchanged:: 0.3

         Before it was called ``new_chat_participant``

   .. py:attribute:: left_chat_member

      A :py:class:`~botogram.User` object representing a member of a group chat
      that has been removed from the group. This user may be a bot.

      *This attribute can be None if it's not provided by Telegram.*

      .. versionchanged:: 0.3

         Before it was called ``left_chat_participant``

   .. py:attribute:: new_chat_title

      The new title of the chat to which this message belongs.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: new_chat_photo

      The new :py:class:`~botogram.Photo` for the chat to which this message
      belongs.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: delete_chat_photo

      When ``True`` indicates that the photo for the chat to which this message
      belongs has been deleted.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: group_chat_created

      When ``True`` indicates that the group as represented by the chat to which
      this message belongs, has been created.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: supergroup_chat_created

      When ``True`` indicates that the supergroup as represented by the chat to
      which this message belongs, has been created.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: channel_chat_created

      When ``True`` indicates that the channel as represented by the chat to
      which this messag belongs, has been created.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: migrate_to_chat_id

      The group has been migrated to the supergroup with the chat_id contained
      in this attribute.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: migrate_from_chat_id

      The supergroup has been migrated from the group with the chat_id
      contained im this attribute.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: pinned_message

      The supergroup has a new pinned :py:class:`~botogram.Message`, which is
      contained in this attribute.

      *This attribute can be None if it's not provided by Telegram.*

      .. versionadded:: 0.3

   .. py:attribute:: new_chat_participant

      Old name for the :py:attr:`~botogram.Message.new_chat_member` attribute.
      Check out its documentation.

      .. deprecated:: 0.3

         It will be removed in botogram 1.0

   .. py:attribute:: left_chat_participant

      Old name for the :py:attr:`~botogram.Message.left_chat_member` attribute.
      Check out its documentation.

      .. deprecated:: 0.3

         It will be removed in botogram 1.0

   .. py:method:: edit(text, [syntax=None, preview=True, attach=None, extra=None])

      With this method you can edit the text of a message the user already
      received. This allows you to do a lot of interesting things, like
      live-updating information or showing paginated results: you just need to
      provide the new **text** of the message, and if you want to show the
      **preview**. The **syntax** parameter is for defining how the message text
      should be processed by Telegram (:ref:`learn more about rich formatting
      <tricks-messages-syntax>`).

      Please remember you can only edit messages your bot sent to the user.

      :param str text: The new text of the message
      :param bool preview: Whether to show link previews.
      :param str syntax: The name of the syntax used for the message.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: delete()

      Delete this message.
      A message can be deleted only if is sent by the bot or sent in a supergroup by an user where the bot is admin.
      It can also be deleted if it's one of the supported service messages.

      .. versionadded:: 0.4

   .. py:method:: edit_caption(caption, [attach=None, extra=None])

      With this method you can edit the caption of the media attached to a
      message the user already received. This allows you to do a lot of
      interesting things, like live-updating information or showing dynamic
      subtitles: you just need to provide the new **caption**.

      Please remember you can only edit messages your bot sent to the user.

      :param str caption: The new caption of the media file.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: edit_attach(attach)

      This method allows you to change the attachment of a message you already
      sent. For example, you can use it to update the :ref:`buttons <buttons>`
      under a message, like so:

      .. code-block:: python

         btns = botogram.Buttons()
         btns[0].url("example.com", "http://example.com")
         message = chat.send("Some example websites.", attach=btns)

         btns[1].url("example.org", "http://example.org")
         message.edit_attach(btns)

      :param object attach: The new attachment

      .. versionadded:: 0.4

   .. py:method:: forward_to(to[, notify=True])

      Forward this message *to* another chat or user by specifying their ID. One
      may also simply pass in the :py:class:`~botogram.Chat` or
      :py:class:`~botogram.User` object without the need to reference the
      object's ID.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int to: The ID of the chat or user this message should forward to.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply(message, [preview=True, syntax=None, attach=None, extra=None, notify=True])

      Reply with the textual *message* in regards to this message. You may
      optionally stop clients from generating a *preview* for any link included
      in the reply. The *syntax* parameter is for defining how the message text
      should be processed by Telegram (:ref:`learn more about rich formatting
      <tricks-messages-syntax>`).

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to reply with.
      :param bool preview: Whether to show link previews.
      :param str syntax: The name of the syntax used for the message.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_photo(path, [caption=None, attach=None, extra=None, notify=True])

      Reply with a photo found at *path* in regards to this message. You may
      optionally specify a *caption* for the photo being sent in reply.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str caption: A caption for the photo.
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_audio(path, [duration=None, performer=None, title=None, attach=None, extra=None, notify=True])

      Reply with the audio track found in the *path* to the chat. You may
      optionally specify the *duration*, the *performer* and the *title* of the
      audio track.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_voice(chat, path, [duration=None, attach=None, extra=None, notify=True])

      Send the voice message found in the *path* to the chat. You may
      optionally specify the *duration* of the voice message.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param int duration: The message duration, in seconds
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_video(path, [duration=None, caption=None, attach=None, extra=None, notify=True])

      Reply with the video found in the *path* to the chat. You may optionally
      specify the *duration* and the *caption* of the video.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_file(path, [attach=None, extra=None, notify=True])

      Reply with the generic file found in the *path* to the chat. If the file
      you're sending is in reply to another message, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_location(latitude, longitude, [attach=None, extra=None, notify=True])

      Send the geographic location to the user.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_venue(latitude, longitude, title, address, [foursquare=None, attach=None, extra=None, notify=True])

      Reply to this message with a venue. A venue is made of its geographic
      coordinates (latitude and longitude), its title and address, and
      optionally the venue's Foursquare ID, if you want to integrate with that.
      Users will then see the venue in the map, along with the information you
      provided.

      You can use this, for example, if you want to recommend to your bot's
      users a place to go to dinner tonight:

      .. code-block:: python

         @bot.command("whereshouldigo")
         def whereshouldigo_command(chat, message, args):
             message.reply("Here there is an unique place to go to dinner tonight!")
             message.reply_with_venue(35, -45, "The Abyss", "Atlantic Ocean")

      :param float latitude: The latitude of the venue
      :param float longitude: The longitude of the venue
      :param str title: The name of the venue
      :param str address: The address of the venue
      :param str foursquare: The Foursquare ID of the venue
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3

   .. py:method:: reply_with_sticker(sticker, [reply_to=None, attach=None, extra=None, notify=True])

      Reply with the sticker (in webp format) to the chat.

      The *attach* parameter allows you to attach extra things like
      :ref:`buttons <buttons>` to the message.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionchanged:: 0.3

         Now the method returns the sent message

   .. py:method:: reply_with_contact(phone, first_name, [last_name=None, attach=None, extra=None, notify=True])

      Reply to this message with a contact. A Telegram contact is made of its
      phone number (with the international prefix), its first name and
      optionally its last name. You can use this, for example, to send the user
      the phone number of a buisness so he can call them:

      .. code-block:: python

         @bot.command("support")
         def support_command(chat, message, args):
             message.reply("Hi there, here is our support number:")
             message.reply_with_contact("+390124567890", "Support")

      :param str phone: The phone number of the contact
      :param str first_name: The first name of the contact
      :param str last_name: The last name of the contact
      :param object attach: An extra thing to attach to the message.
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger a notification on the client
      :returns: The message you sent
      :rtype: ~botogram.Message

      .. deprecated:: 0.4

         The *extra* parameter is now deprecated

      .. versionadded:: 0.3


.. py:class:: botogram.Photo

   This class provides a general representation of a photo received by your bot.

   Photos are usually available in different resolutions, and objects of this
   class provide easy access to the various sized photos which are available.
   As convenience, an object of this class also represents the photo with the
   greatest resolution available. You can also access a list of the
   :py:class:`~botogram.PhotoSize` objects representing every resolution
   available, as well as the :py:class:`~botogram.PhotoSize` object of the
   greatest and lowest resolutions specifically.

   .. py:attribute:: file_id

      The string ID of the file with the greatest available resolution. You can
      use this to uniquely reference this specific sized photo.

   .. py:attribute:: width

      The integer width of the photo with the greatest available resolution.

   .. py:attribute:: height

      The integer height of the photo with the greatest available resolution.

   .. py:attribute:: file_size

      The integer size of the file representing the photo with the greatest
      available resolution.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: biggest

      A reference to the :py:class:`~botogram.PhotoSize` object of the file with
      the greatest available resolution. As convenience a
      :py:class:`~botogram.Photo` also represents this biggest available file.

   .. py:attribute:: smallest

      A reference to the :py:class:`~botogram.PhotoSize` object of the file with
      the lowest available resolution. Use this for obtaining the smallest
      available file.

   .. py:attribute:: sizes

      A list of :py:class:`~botogram.PhotoSize` objects, representing all the
      different available resolutions of the photo.

   .. py:method:: save(path)

      Save the photo of highest available resolution to a file located by
      *path*. Be aware that Telegram does not provide the name of the original
      file sent by its sender. This should be generated as part of the path.

      :param str path: The file name path locating where the photo should be saved.


.. py:class:: botogram.PhotoSize

   This class represents a single resolution of a photo received by your bot.

   This means for each photo the bot will receive, it will get multiple
   instances of this object, one of each resolution available.

   Despite its name, objects of this class are also used to describe images of
   various Telegram API objects, including :py:class:`~botogram.UserProfilePhotos`
   and thumbnail images for the :py:class:`~botogram.Document`,
   :py:class:`~botogram.Sticker`, and :py:class:`~botogram.Video` classes.

   See the :py:class:`botogram.Photo` class for a more friendly way to work
   with photos specifically.

   .. py:attribute:: file_id

      The string ID of the file. Use this to uniquely reference this specific
      image.

   .. py:attribute:: width

      The integer width of the image represented.

   .. py:attribute:: height

      The integer height of the image represented.

   .. py:attribute:: file_size

      The integer size of the file represented.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the image represented to a file located by *path*. Be aware that
      Telegram does not provide the name of the original file sent by its
      sender. This should be generated as part of the path.

      :param str path: The file name path locating where the image should be saved.


.. py:class:: botogram.Audio

   This class represents an audio track, a file meant to be treated as music by
   Telegram clients.

   .. py:attribute:: file_id

      The string ID of the file.

   .. py:attribute:: duration

      The integer duration in seconds of the audio as defined by the sender.

   .. py:attribute:: performer

      Performer of the audio. May be defined by the sender, or from audio tags.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: title

      Title of the audio. May be defined by the sender, or from audio tags.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: mime_type

      MIME type of the audio file as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_size

      The integer size of the audio file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the audio track to a file located by *path*. Be aware that Telegram
      does not provide the name of the original file sent by its sender. This
      should be generated as part of the path.

      :param str path: The file name path locating where the audio should be saved.


.. py:class:: botogram.Document

   This class represents a general file. Other objects of this API may be used
   instead in order to take advantage of client side features for common file
   types, such as with :py:class:`~botogram.Audio`, :py:class:`~botogram.Photo`,
   :py:class:`~botogram.Video` and :py:class:`~botogram.Voice`. Use this class
   when working with all other file types, or for when you do not want clients
   to offer specialized features for the type.

   .. py:attribute:: file_id

      The string ID of the file.

   .. py:attribute:: thumb

      A :py:class:`~botogram.PhotoSize` object representing a thumbnail image of
      the file as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_name

      Intended to be the original file name as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: mime_type

      MIME type of the file as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_size

      The integer size of the file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the file to a file located by *path*. Be aware that Telegram does not
      provide the name of the original file sent by its sender. This should be
      generated as part of the path.

      :param str path: The file name path locating where the file should be saved.


.. py:class:: botogram.Sticker

   This class represents a sticker image.

   .. py:attribute:: file_id

      The string ID of the file.

   .. py:attribute:: width

      The integer width of the sticker image.

   .. py:attribute:: height

      The integer height of the sticker image.

   .. py:attribute:: thumb

      A :py:class:`~botogram.PhotoSize` object representing a thumbnail image of
      the file as defined by the sender (in .webp or .jpg format).

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: emoji

      The unicode emoji related to the sticker. This is set by the author of
      the sticker, and it's completly arbitrary.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_size

      The integer size of the file represented.

      *This attribute can be None if it's not provided by Telegram.*


.. py:class:: botogram.Video

   This class represents a video file.

   .. py:attribute:: file_id

      The string ID of the file.

   .. py:attribute:: width

      The integer width of the video as defined by the sender.

   .. py:attribute:: height

      The integer height of the video as defined by the sender.

   .. py:attribute:: duration

      The integer duration in seconds of the video as defined by the sender.

   .. py:attribute:: thumb

      A :py:class:`~botogram.PhotoSize` object representing a thumbnail image of
      the video as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: mime_type

      MIME type of the video file as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_size

      The integer size of the video file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the video to a file located by *path*. Be aware that Telegram does
      not provide the name of the original file sent by its sender. This should
      be generated as part of the path.

      :param str path: The file name path locating where the video should be saved.


.. py:class:: botogram.Voice

   This class represents a voice message.

   .. py:attribute:: file_id

      The string ID of the file.

   .. py:attribute:: duration

      The integer duration in seconds of the voice message defined by the
      sender.

   .. py:attribute:: mime_type

      MIME type of the voice message as defined by the sender.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: file_size

      The integer size of the voice message file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the voice message to a file located by *path*. Be aware that Telegram
      does not provide the name of the original file sent by its sender. This
      should be generated as part of the path.

      :param str path: The file name path locating where the voice message should be saved.


.. py:class:: botogram.Contact

   This class represents a phone contact.

   .. py:attribute:: phone_number

      The string phone number of the contact.

   .. py:attribute:: first_name

      The first name of the contact.

   .. py:attribute:: last_name

      The last name of the contact.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: user_id

      The integer user ID of the contact in Telegram.

      *This attribute can be None if it's not provided by Telegram.*


.. py:class:: botogram.Location

   This class represents a point located on Earth.

   .. py:attribute:: longitude

      The float longitude as defined by the sender.

   .. py:attribute:: latitude

      The float latitude as defined by the sender.


.. py:class:: botogram.Venue

   This object represents a venue (a location with attached a title and an
   address). A venue may also have a Foursquare ID attached.

   .. py:attribute:: location

      The :py:class:`~botogram.Location` of the venue. You can use this to get
      the exact geographic coordinates of the venue.

   .. py:attribute:: title

      The name of the venue. The value might not match the venue sometimes,
      because it's supplied by the user/bot who sent the venue.

   .. py:attribute:: address

      The address of the venue. The value might not match the venue sometimes,
      because it's supplied by the user/bot who sent the venue.

   .. py:attribute:: foursquare

      The ID of the venue on Foursquare. You can use this to get more
      information about the venue from the Foursquare API. The ID might not
      match the venue sometimes because it's supplied by the user/bot who sent
      the venue.

      *This value can be None if the venue doesn't have a Foursquare ID.*


.. py:class:: botogram.Update

   This class represents an update received by the bot. You should not need to
   work with objects of this type unless you are building a highly modified bot
   runner, or the like.

   .. py:attribute:: update_id

      The unique integer ID of the update. Update IDs always start at a positive
      number and increase sequentially.

   .. py:attribute:: message

      The encapsulating :py:class:`~botogram.Message` object, which wraps the
      vast majority of API objects.

      *This attribute can be None if it's not provided by Telegram.*


.. py:class:: botogram.UserProfilePhotos

   This class represents the photos of a user's profile.

   .. py:attribute:: total_count

      The integer number of photos a user has in their profile.

   .. py:attribute:: photos

      A list of :py:class:`~botogram.PhotoSize` objects, representing all photos
      in the user's profile, with up to 4 differing sizes of each.


.. py:class:: botogram.ReplyKeyboardMarkup

   This class represents a custom keyboard with reply options. Objects of this
   class are passed along to messaging methods as the value to the *extra*
   parameter. Each defines an easy to use reply interface, greatly simplifying
   user interaction with you bot. These custom keyboards can help make
   interacting with your bot more conversational, rather than command oriented.

   .. py:attribute:: keyboard

      A list of button rows, with each row defined by a list of strings,
      each defining the label of a button.

   .. py:attribute:: resize_keyboard

      When ``True`` requests that clients reduce the vertical size of the
      keyboard so that it takes up a minimal amount of space. Useful for
      keyboards with few rows.

      *Defaults to* ``False``, and the keyboard will take up the same amount of
      vertical space as the client's standard keyboard.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: one_time_keyboard

      When ``True`` requests that clients hide the keyboard as soon as it's been
      used.

      *Defaults to* ``False``.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: selective

      When ``True`` show the keyboard only to selective users. Users selected to
      receive the keyboard are:

         * Those mentioned by @username in the text of the message object.
         * The sender of the original message, when the message this object
           is attached to is made in reply.

      *This attribute can be None if it's not provided by Telegram.*


.. py:class:: botogram.ReplyKeyboardHide

   By default, when your bot sends :py:class:`~botogram.ReplyKeyboardMarkup`
   along with a message, the resulting custom keyboard is shown until a new
   keyboard is sent by a bot. This class represents objects used to configure
   messages to hide any currently showing custom keyboard, and to instead
   display the client's standard keyboard. Objects of this class are passed
   along to messaging methods as the value to the *extra* parameter.

   .. py:attribute:: hide_keyboard

      When ``True`` request clients to hide any custom keyboard currently shown.

   .. py:attribute:: selective

      When ``True`` hide only the custom keyboards of selective users. Users
      selected to hide their keyboards are:

         * Those mentioned by @username in the text of the message object.
         * The sender of the original message, when the message this object
           is attached to is made in reply.

      *This attribute can be None if it's not provided by Telegram.*


.. py:class:: botogram.ForceReply

   This class represents objects used to force a user to reply to a message
   sent to them by your bot. Objects of this class are passed along to messaging
   methods as the value to the *extra* parameter. When a user receives a message
   configured with a ForceReply object, the user's client will display a reply
   interface to the user, effectively as if they had selected the bot's message
   and chose to reply.

   .. py:attribute:: force_reply

      When ``True`` show the reply interface to the user, as if they had
      selected the bot's message and chose to 'Reply'.

   .. py:attribute:: selective

      When ``True`` force only selective users to reply. Users selected to force
      reply are:

         * Those mentioned by @username in the text of the message object.
         * The sender of the original message, when the message this object
           is attached to is made in reply.

      *This attribute can be None if it's not provided by Telegram.*


.. _Telegram's Bot API: https://core.telegram.org/bots/api
.. _API methods: https://core.telegram.org/bots/api#available-methods
.. _API types: https://core.telegram.org/bots/api#available-types
