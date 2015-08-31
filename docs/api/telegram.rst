.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _api-telegram:

~~~~~~~~~~~~~~~~~~~~
Telegram API wrapper
~~~~~~~~~~~~~~~~~~~~

botogram wraps the Telegram API in order to give you better tools, and to
provide a better representation of the information Telegram gives to your bot.
Here you can see all the available classes and objects.


.. py:class:: botogram.User

   This class represents a Telegram user.

   .. py:attribute:: id

      The ID of the user

   .. py:attribute:: first_name

      The first name of the user

   .. py:attribute:: last_name

      The last name of the user

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: username

      The user's username, without the ``@`` prefix.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: send(message, [preview=True, reply_to=None, extra=None])

      Send a message to the user. You can also define if a preview for links
      should be showed (yes by default), the message ID of the message this one
      is replying to, and an extra object. One of these extra can be provided
      as the extra one:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      :param str message: The message you want to send
      :param bool preview: Show the link preview
      :param int reply_to: The ID of the message this one is replying to
      :param object extra: An extra object you want to attach (see above)

.. py:class:: botogram.GroupChat

   This class represents a Telegram's group chat.

   .. py:attribute:: id

      The ID of the group chat

   .. py:attribute:: title

      The title of the group chat

   .. py:method:: send(message, [preview=True, reply_to=None, extra=None])

      Send a message to the group chat. You can also define if a preview for
      links should be showed (yes by default), the message ID of the message
      this one is replying to, and an extra objects. One of these extra objects
      can be provided:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      :param str message: The message you want to send
      :param bool preview: Show the link preview
      :param int reply_to: The ID of the message this one is replying to
      :param object extra: An extra object you want to attach (see above)
