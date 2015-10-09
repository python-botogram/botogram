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

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, extra=None])

      Send a message to the user. You can also define if a preview for links
      should be showed (yes by default), the message ID of the message this one
      is replying to, and an extra object. One of these extra can be provided
      as the extra one:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The syntax parameter contains how the message should be processed by
      Telegram, and it can be either ``plain`` (no syntax) or ``markdown``. If
      you don't provide it, botogram will try to guess which syntax to use by
      parsing the message you want to send. This feature is not supported by
      all the Telegram clients.

      :param str message: The message you want to send
      :param bool preview: Show the link preview
      :param int reply_to: The ID of the message this one is replying to
      :param string syntax: The name of the syntax you used for the message.
      :param object extra: An extra object you want to attach (see above)

.. py:class:: botogram.GroupChat

   This class represents a Telegram's group chat.

   .. py:attribute:: id

      The ID of the group chat

   .. py:attribute:: title

      The title of the group chat

   .. py:method:: send(message, [preview=True, reply_to=None, syntax=None, extra=None])

      Send a message to the group chat. You can also define if a preview for
      links should be showed (yes by default), the message ID of the message
      this one is replying to, and an extra objects. One of these extra objects
      can be provided:

      * :py:class:`botogram.ReplyKeyboardMarkup`
      * :py:class:`botogram.ReplyKeyboardHide`
      * :py:class:`botogram.ForceReply`

      The syntax parameter contains how the message should be processed by
      Telegram, and it can be either ``plain`` (no syntax) or ``markdown``. If
      you don't provide it, botogram will try to guess which syntax to use by
      parsing the message you want to send. This feature is not supported by
      all the Telegram clients.

      :param str message: The message you want to send
      :param bool preview: Show the link preview
      :param int reply_to: The ID of the message this one is replying to
      :param string syntax: The name of the syntax you used for the message.
      :param object extra: An extra object you want to attach (see above)

.. py:class:: botogram.Photo

   This class provides a representation of a photo sent to your bot by someone.

   Photos are usually available in different resolutions, and this class
   provides you the file with the biggest resolution available. You can also
   get the :py:class:`botogram.PhotoSize` of every resolution available, and
   the :py:class:`botogram.PhotoSize` of the files with the greatest and
   lowest resolutions.

   .. py:attribute:: file_id

      The ID of the file with the greatest resolution available. You can use
      this to uniquely reference a photo.

   .. py:attribute:: width

      The width of the photo, in the file with the greates resolution
      available.

   .. py:attribute:: height

      The height of the photo, in the file with the greatest resolution
      available.

   .. py:attribute:: file_size

      The size of the file with the greatest resolution available.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: biggest

      This attribute contains a reference to the :py:class:`botogram.PhotoSize`
      of the file with the greatest resolution available. You can use this if
      you specifically wants the greatest resolution.

   .. py:attribute:: smallest

      This attribute contains a reference to the :py:class:`botogram.PhotoSize`
      of the file with the lowest resolution available. You can use this if
      you specifically wants the lowest resolution.

   .. py:attribute:: sizes

      This attribute contains a list of the :py:class:`botogram.PhotoSize` of
      all the different resolutions available.

   .. py:method:: save(path)

      Save the photo to the provided path. The file with the greatest
      resolution will be downloaded there. Please note that Telegram doesn't
      provide the name of the original file the user sent, so you should
      generate it by yourself.

      :param str path: Where you want to save the file

.. py:class:: botogram.PhotoSize

   This class represents a single resolution of a photo received by your bot.
   This means for each photo your bot will receive, you'll get multiple
   instances of this object, one of each resolution available.

   .. py:attribute:: file_id

      The ID of the file. You can use this to uniquely reference a resolution
      of a photo.

   .. py:attribute:: width

      The width of the file.

   .. py:attribute:: height

      The height of the file.

   .. py:attribute:: file_size

      The size of the file.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: save(path)

      Save the file to the provided path. The file will be downloaded there.
      Please note that Telegram doesn't provide the name of the original file
      the user sent, so you should generate it by yourself.

      :param str path: Where you want to save the file
