.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _api-buttons:

=========================
Buttons and callbacks API
=========================

This page contains the documentation for the APIs related to buttons and
callbacks. See the :ref:`narrative chapter about them <buttons>` for more
information about them.


.. py:class:: botogram.Buttons

   This class allows you to build buttons to attach to messages. You must use
   it as a list, accessing the various rows with the square brackets.

   Each element of this simulated list is automatically created the first time
   you access it, and it's an instance of :py:class:`~botogram.ButtonsRow`: you
   can use that object to actually populate the buttons. Check out that class'
   documentation for all the buttons you can add.

   Then, you can send the buttons by attaching them to an outgoing message, as
   shown in the example below. You can also reuse the same instance for
   multiple messages.

   .. code-block:: python

      @bot.command("example")
      def example_command(chat, message, args):
          """Show some example sites"""
          btns = botogram.Buttons()
          btns[0].url("Visit example.com", "http://www.example.com")
          btns[1].url("example.net", "http://www.example.net")
          btns[1].url("example.org", "http://www.example.org")

          chat.send("Check out some example sites!", attach=btns)

   .. versionadded:: 0.4


.. py:class:: botogram.ButtonsRow

   This class represents a row in a set of buttons: you can use it to add the
   individual buttons to it. You should not create an instance of this class
   directly, but you should get them through the :py:class:`~botogram.Buttons`
   class.

   .. versionadded:: 0.4

   .. py:method:: callback(label, callback, [data=None])

      Add a new button to the row, which will call the corresponding callback
      when pressed by the user. You need to provide the label of the button,
      the name of the callback and an optional string of data, which will be
      passed to the callback.

      Due to limitations in the Telegram Bot API, you can provide in the
      *data* argument a maximum of 32 bytes of text: an exception will be
      raised if you provide more.

      The information contained in the callback will automatically be signed by
      botogram, to prevent tampering, but the data is **not** encrypted: an
      user with a special client might be able to see it, without being able to
      change it. See :ref:`the security section <buttons-security>` for more
      details.

      .. code-block:: python

         btns = botogram.Buttons()
         btns[0].callback("Commit changes", "commit")
         btns[0].callback("Checkout master", "checkout", "master")

      :param str label: The label of the button shown to the user
      :param str callback: The internal name of the callback
      :param str data: Extra data provided to the callback (max 32 bytes)

   .. py:method:: url(label, url)

      Add a new button to the row, which will ask the user if they want to open
      the URL you provided. If they agree, the url will be opened in the user's
      browser. You need to provide the label of the button and the URL.

      .. code-block:: python

         btns = botogram.Buttons()
         btns[0].url("See example.com", "http://www.example.com")

      :param str label: The label of the button shown to the user
      :param str url: The URL the user should open when the button is pressed

   .. py:method:: switch_inline_query(label, [query="", current_chat=False])

      Add a new button to the row, which will switch the user to the inline
      query mode of the bot. You need to provide the label of the button, and
      optionally the query that should be prefilled in the user's search field.

      If *current_chat* is False, the user will be asked in which chat the
      inline query should be opened. If you set it to True, the inline query
      will be opened in the current chat.

      .. code-block:: python

         btns = botogram.Buttons()
         btns[0].switch_inline_query("Show pictures of cats to your friends!", "cats")

      :param str label: The label of the button shown to the user
      :param str query: Default query provided to the user
      :param bool current_chat: Open in the current chat instead of asking the
         user to select one


.. py:class:: botogram.CallbackQuery

   This class represents a callback query received from Telegram. It contains
   all the information you need about it, and allows you to respond to it.

   .. versionadded:: 0.4

   .. py:attribute:: id

      The unique ID of this callback query. You might need to use it if you
      interact with the Bot API directly.

   .. py:attribute:: sender

      The :py:class:`~botogram.User` who sent the query.

   .. py:attribute:: message

      The :py:class:`~botogram.Message` with the button that originated the
      callback.

   .. py:attribute:: chat_instance

      An unique string identifying the chat where the message with the button
      that called the callback is.

   .. py:attribute:: inline_message_id

      An unique string identifying the inline message with the button that
      originated the callback.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:attribute:: game_short_name

      The short name of the Telegram Game that the user requested to play.

      *This attribute can be None if it's not provided by Telegram.*

   .. py:method:: notify(text, [alert=False, cache=0])

      Send a notification to the user that pressed the button originating the
      callback. You need to provide the text of the notification and,
      optionally, for how long the action will be cached by the client.

      If *alert* is True, the user will be shown an alert window with the
      message. Otherwise, the message will be displayed as the client likes,
      for example as a toast.

      .. code-block:: python

         @bot.callback("say-hi")
         def say_hi_callback(query):
            query.notify("Hi " + query.sender.name + "!")

      :param str text: The content of the notification
      :param bool alert: Show the notification as an alert to the user
      :param int cache: How long the client should cache the response

   .. py:method:: open_url(url, [cache=0])

      Tell the user's client to open an URL in the browser. This action is
      currently restricted only to the bots that agreed the Telegram Games
      Terms of Service: check out `the Telegram documentation`_ for more
      information about games.

      You need to provide the URL of the page, and optionally how long you want
      the client to cache the action.

      .. code-block:: python

         @bot.callback("open-game")
         def open_game(query):
             query.open_url("http://game.example.com")

      :param str url: The URL you want the user to open
      :param int cache: How long the client should cache the response

      .. _the Telegram documentation: https://core.telegram.org/bots/api#games

   .. py:method:: open_private_chat(start_arg, [cache=0])

      Tell the user's client to open a private chat with the bot, and to switch
      to it. You need to provide a non-empty start argument, which will be
      appended to the ``/start`` command the client will send (but it won't be
      displayed to the user). Optionally, you can provide how long you want the
      client to cache the action.

      .. code-block:: python

         @bot.open("show-help")
         def show_help(query):
             query.open_private_chat("show-help-to-the-user")

         @bot.command("start")
         def start_command(chat, message, args):
             if len(args) == 1 and args[0] == "show-help-to-the-user":
                 chat.send("This is the help message of the bot.")
             else:
                 chat.send("Hi! I'm a bot")

      :param str start_arg: The argument to provide to ``/start``
      :param int cache: How long the client should cache the response
