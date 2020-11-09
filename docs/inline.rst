.. Copyright (c) 2015-2020 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _inline:

===========
Inline mode
===========

Inline bots allow using bot services in any chat without adding them as members – you just type the bot username followed by your message and everything that comes after becomes an inline query.
To enable the inline mode on your bots and receive updates you need to talk to `BotFather <https://t.me/BotFather>`_.


Create your first inline article
--------------------------------
For receving inline updates, you can add your hook under :py:meth:`botogram.Bot.inline`.
The following example is a simple inline hook:

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
      yield inline.article(
          "Hello World",
          content=botogram.InlineInputMessage("My first inline response with botogram")
      )

When the bot receives an inline update, it will render one inline :py:meth:`~botogram.InlineQuery.article` with the specified *title* and *content*.
The *content* is what is sent when the user clicks on the result.

Handle query strings
--------------------

Everything the user writes after the bot username is called *query* or *query string*. It can also be an empty string.
Let's see how we can handle it:

.. code-block:: python

  @bot.inline
  def inline_processor(inline, query):
      if query is "hello":
          yield inline.article(
              "Hello friend",
              content=botogram.InlineInputMessage("I wrote \"hello\"!")
          )
      else:
          yield inline.article(
              "Write \"hello\"",
              content=botogram.InlineInputMessage(f"I didn't write \"hello\", but I wrote {inline.query}")
          )


You can either use the ``query`` parameter in the hook or the :py:attr:`~botogram.InlineQuery.query` attribute.

Pagination
----------

When rendering large amounts of results, you may want to paginate them so you can control how many results are rendered at a time.
A higher value means more load on your server for request but a lower value can be tedious for the user to scroll through (and even cause bugs).
We suggest never going under 5 results for page.

.. code-block:: python

  @bot.inline(paginate=10)
  def inline_processor(inline):
      for i in range(100):
          if i == 20:
              inline.paginate = 20
          yield inline.article(
              f"Result #{i}",
              content=botogram.InlineInputMessage("Hello World message " + str(i))
          )

In the example above you can see that we added a :py:attr:`~botogram.InlineQuery.query.paginate` parameter to the :py:attr:`~botogram.InlineQuery.query` decorator;
this indicates the inital (global) value of pagination. 
We can change it later (in our case after 20 iterations) by assigning an int value to :py:attr:`~botogram.InlineQuery.paginate`, botogram will handle the new value smoothly.


Caching
-------
The **cache** parameter indicates the maximum amount of time in seconds that the result of the inline query
may be cached on Telegram servers (defaults to 300). You can change the parameter at any time.

.. code-block:: python

  @bot.inline(cache=500)
  def inline_caching(sender, query, inline):
      yield inline.article(...)
      inline.cache = 100
      yield inline.article(...)


Results privacy
---------------

The **private** parameter is used to choose if you want to cache the data for all users or just for the sending user.
For instance, if you're exposing personal results for each of your users you should set the private to ``True``.
As all parameters, you can change the value at any time.

In the following example the first article is cached by Telegram, while the others not.

.. code-block:: python

  @bot.inline(private=True)
  def inline_private(sender, query, inline):
      yield inline.article(f"Your ID: {sender.id}", botogram.InlineInputMessage("This message is cached only for you"))
      inline.private = False
      yield inline.article("Hello World", botogram.InlineInputMessage("This message is cached for all users"))


Working with buttons
-----------------

In the following example you can see how buttons works with inline mode, plus some differences compared to non-inline buttons.

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
      btns = botogram.buttons()
      btns[0].url("botogram docs", "https://botogram.dev/")
      btns[0].callback("Click on this button", "button")
      yield inline.article("Hello World", content=botogram.InlineInputMessage("Hello World message"), attach=btns)


  @bot.callback("button")
  def button_callback(message):
      if message.is_inline:
          message.edit("This is a message sent via the inline mode.")
          print(message.is_inline)  # True
          print(message.date)  # None
          print(message.chat)  # None
          print(message.id)  # None
          print(message.inline_message_id)  # Some random unique string
          message.reply("I can't do this!")  # This throws an exception



How :py:meth:`~botogram.ButtonsRow.switch_inline_query` works
------------------------------------------

In the following example we will see how the ``switch_inline_query`` button works.
This type of button switches the mode of the user who clicks it to inline mode.

For more details see :py:meth:`~botogram.ButtonsRow.switch_inline_query`.

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
      btns = botogram.buttons()
      btns[0].url("botogram docs", "https://botogram.dev/")
      yield inline.article("Some cool framework", content=botogram.InlineInputMessage("Hello world!"), attach=btns)


  @bot.command("start")
  def button_callback(chat):
      btns = botogram.buttons()
      btns[0].switch_inline_query("Try the bot in inline mode!", current_chat=True)
      chat.send("Click the button below", attach=btns)


Inline feedbacks
----------------

If you have many users, maybe you want to acquire statistics or do something about which elements are chosen by the user
in the inline results page.
You can specify how many (in percentage) inline feedbacks do you want to get via BotFather with the ``/setinlinefeedback`` command;
you'll then receive an update when the user *clicks* on a inline result.

For more details see :py:class:`~botogram.InlineFeedback`.

.. code-block:: python

  @bot.inline_feedback
  def inline_feedback(feedback):
      print(f"User {feedback.sender.id} has clicked result_id #{feedback.result_id} with query {feedback.query}!")


.. versionadded:: 0.7
