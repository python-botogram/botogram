.. Copyright (c) 2015 Brad Christensen <temporalsculpt@live.com>
   Released under the MIT license

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

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, extra=None, notify=True])

      Send the textual *message* to the user. You may optionally stop clients
      from generating a *preview* for any link included in the message. If the
      message you are sending is in reply to another, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`. The *syntax* parameter is for
      defining how the message text should be processed by Telegram
      (:ref:`learn more about rich formatting <tricks-messages-syntax>`).
      *extra* is an optional object which specifies additional reply interface
      options on the recipient's end, and can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to be sent.
      :param bool preview: Whether to show link previews.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param str syntax: The name of the syntax used for the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_photo(path, [caption=None, reply_to=None, extra=None, notify=True])

      Send a photo found at *path* to the user. You may optionally specify a
      *caption* for the photo being sent. If the photo you are sending is in
      reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`. *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str caption: A caption for the photo.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_audio(path, [duration=None, performer=None, title=None, reply_to=None, extra=None, notify=True])

      Send the audio track found in the *path* to the user. You may optionally
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

      :param str path: The path to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_voice(chat, path, [duration=None, reply_to=None, extra=None, notify=True])

      Send the voice message found in the *path* to the user. You may
      optionally specify the *duration* of the voice message. If the voice
      message you're sending is in reply to another message, set *reply_to* to
      the ID of the other :py:class:`~botogram.Message`.  *extra* is an
      optional object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param int duration: The message duration, in seconds
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_video(path, [duration=None, caption=None, reply_to=None, extra=None, notify=True])

      Send the video found in the *path* to the user. You may optionally
      specify the *duration* and the *caption* of the video. If the audio track
      you're sending is in reply to another message, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`.  *extra* is an optional
      object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_file(path, [reply_to=None, extra=None, notify=True])

      Send the generic file found in the *path* to the user. If the file you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_location(latitude, longitude, [reply_to=None, extra=None, notify=True])

      Send the geographic location to the user. If the location you're sending
      is in reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_sticker(sticker, [reply_to=None, extra=None, notify=True])

      Send the sticker to the user (in webp format). If the sticker you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`. *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.


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

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, extra=None, notify=True])

      Send the textual *message* to the chat. You may optionally stop clients
      from generating a *preview* for any link included in the message. If the
      message you are sending is in reply to another, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`. The *syntax* parameter is for
      defining how the message text should be processed by Telegram
      (:ref:`learn more about rich formatting <tricks-messages-syntax>`).
      *extra* is an optional object which specifies additional reply interface
      options on the recipient's end, and can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to be sent.
      :param bool preview: Whether to show link previews.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param str syntax: The name of the syntax used for the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_photo(path, [caption=None, reply_to=None, extra=None, notify=True])

      Send a photo found at *path* to the chat. You may optionally specify a
      *caption* for the photo being sent. If the photo you are sending is in
      reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`. *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str caption: A caption for the photo.
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_audio(path, [duration=None, performer=None, title=None, reply_to=None, extra=None, notify=True])

      Send the audio track found in the *path* to the chat. You may optionally
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

      :param str path: The path to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_voice(chat, path, [duration=None, reply_to=None, extra=None, notify=True])

      Send the voice message found in the *path* to the chat. You may
      optionally specify the *duration* of the voice message. If the voice
      message you're sending is in reply to another message, set *reply_to* to
      the ID of the other :py:class:`~botogram.Message`.  *extra* is an
      optional object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param int duration: The message duration, in seconds
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_video(path, [duration=None, caption=None, reply_to=None, extra=None, notify=True])

      Send the video found in the *path* to the chat. You may optionally
      specify the *duration* and the *caption* of the video. If the audio track
      you're sending is in reply to another message, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`.  *extra* is an optional
      object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_file(path, [reply_to=None, extra=None, notify=True])

      Send the generic file found in the *path* to the chat. If the file you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_location(latitude, longitude, [reply_to=None, extra=None, notify=True])

      Send the geographic location to the chat. If the location you're sending
      is in reply to another message, set *reply_to* to the ID of the other
      :py:class:`~botogram.Message`.  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_sticker(sticker, [reply_to=None, extra=None, notify=True])

      Send the sticker to the chat (in webp format). If the sticker you're
      sending is in reply to another message, set *reply_to* to the ID of the
      other :py:class:`~botogram.Message`. *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param int reply_to: The ID of the :py:class:`~botogram.Message` this one is replying to
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

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

      The sending :py:class:`~botogram.User` of the original message when this
      message is a forward.

      *This attribute can be None if it's not provided by Telegram.*

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

   .. py:attribute:: new_chat_participant

      A :py:class:`~botogram.User` object representing a new participant to a
      group chat. This user may be a bot.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: left_chat_participant

      A :py:class:`~botogram.User` object representing a participant in a group
      chat that has been removed from the group. This user may be a bot.

      *This attribute can be None if it's not provided by Telegram.*

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

   .. py:method:: forward_to(to[, notify=True])

      Forward this message *to* another chat or user by specifying their ID. One
      may also simply pass in the :py:class:`~botogram.Chat` or
      :py:class:`~botogram.User` object without the need to reference the
      object's ID.

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param int to: The ID of the chat or user this message should forward to.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply(message, [preview=True, syntax=None, extra=None, notify=True])

      Reply with the textual *message* in regards to this message. You may
      optionally stop clients from generating a *preview* for any link included
      in the reply. The *syntax* parameter is for defining how the message text
      should be processed by Telegram (:ref:`learn more about rich formatting
      <tricks-messages-syntax>`).  *extra* is an optional object which
      specifies additional reply interface options on the recipient's end, and
      can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str message: The textual message to reply with.
      :param bool preview: Whether to show link previews.
      :param str syntax: The name of the syntax used for the message.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_photo(path, [caption=None, extra=None, notify=True])

      Reply with a photo found at *path* in regards to this message. You may
      optionally specify a *caption* for the photo being sent in reply. *extra*
      is an optional object which specifies additional reply interface options
      on the recipient's end, and can be one of the following types:

        * :py:class:`botogram.ReplyKeyboardMarkup`
        * :py:class:`botogram.ReplyKeyboardHide`
        * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the photo.
      :param str caption: A caption for the photo.
      :param object extra: An extra reply interface object to attach.
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_audio(path, [duration=None, performer=None, title=None, extra=None, notify=True])

      Reply with the audio track found in the *path* to the chat. You may
      optionally specify the *duration*, the *performer* and the *title* of the
      audio track. *extra* is an optional object which specifies additional
      reply interface options on the recipient's end, and can be one of the
      following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the audio track
      :param int duration: The track duration, in seconds
      :param str performer: The name of the performer
      :param str title: The title of the track
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_voice(chat, path, [duration=None, extra=None, notify=True])

      Send the voice message found in the *path* to the chat. You may
      optionally specify the *duration* of the voice message. *extra* is an
      optional object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the voice message
      :param int duration: The message duration, in seconds
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: send_video(path, [duration=None, caption=None, extra=None, notify=True])

      Reply with the video found in the *path* to the chat. You may optionally
      specify the *duration* and the *caption* of the video. *extra* is an
      optional object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the video
      :param int duration: The video duration, in seconds
      :param str caption: The caption of the video
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_file(path, [extra=None, notify=True])

      Reply with the generic file found in the *path* to the chat. If the file
      you're sending is in reply to another message, set *reply_to* to the ID
      of the other :py:class:`~botogram.Message`.  *extra* is an optional
      object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str path: The path to the file
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_location(latitude, longitude, [extra=None, notify=True])

      Send the geographic location to the user. *extra* is an optional object
      which specifies additional reply interface options on the recipient's
      end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param float latitude: The latitude of the location
      :param float longitude: The longitude of the location
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.

   .. py:method:: reply_with_sticker(sticker, [reply_to=None, extra=None, notify=True])

      Reply with the sticker (in webp format) to the chat. *extra* is an
      optional object which specifies additional reply interface options on the
      recipient's end, and can be one of the following types:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The *notify* parameter is for defining if your message should trigger
      a notification on the client side (yes by default).

      :param str sticker: The path to the webp-formatted sticker
      :param object extra: An extra reply interface object to attach
      :param bool notify: If you want to trigger the client notification.


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
