.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
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

When rendering large amounts of results, you may wish to paginate them so you can control how many results are rendered at a time.
A higher value means more load on your server for request but a lower value can be tedious for the user to scroll through (and even cause bugs). We suggest never going under 5 results for page .

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


Setting private to true the query will be cached for all the users.
Also if private=true the query is cached for **all users**
#TODO consigli come usare sta cosa qua

.. code-block:: python

  @bot.inline(private=True)
  def inline_private(sender, query, inline):
      yield inline.article("Hello World",
                              botogram.InlineInputMessage("Hello world message"))
      inline.private = False
      yield inline.article("Hello World don't cache",
                          botogram.InlineInputMessage(
                            "Hello world message don't cache"))

In this example the firts article is cached by telegram, while the other article is not.


Work with buttons
-----------------

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
    btns = botogram.buttons()
    btns[0].url("botogram docs", "https://botogram.dev/")
    btns[0].callback("text of message", "button")
    yield inline.article("Hello World",content=botogram.InlineInputMessage("Hello World message"),attach=btns)

    message.is_inline
  @bot.callback("button")
  def button_callback(message):
      message.edit("edit message")

In this example you can see how buttons works with ``Inline Mode``, plus some differences compared to non-inline buttons.

Some differences are: ``message.date`` returns ``None``, ``message.chat`` returns ``None``, now it exists a new parameter, ``message.is_inline`` (Returns True if it is from an inline message, else it returns False), ``message.id`` returns the id of the inline message (**the reply function does not work with the inline mode**)

In this example code you can see how the buttons in the ``Inline Mode`` works. You can see that it changes a little from non-inline buttons, the only difference is that the chat parameter in callback is none.

How :py:meth:`~botogram.ButtonsRow.switch_inline_query` works
------------------------------------------

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
    btns = botogram.buttons()
    btns[0].url("botogram docs", "https://botogram.dev/")
    yield inline.article("Hello World",content=botogram.InlineInputMessage("Hello World message"),attach=btns)


  @bot.command("start")
  def button_callback(chat):
      btns = botogram.buttons()
      btns[0].switch_inline_query("test me" 
      current_chat=True)
      chat.send("Click the button below", attach=btns)

In this example we will see how the ``switch_inline_query`` button works. This type of button switches the mode of the user who clicks it to inline mode. For more details click :py:meth:`~botogram.ButtonsRow.switch_inline_query`


.. versionadded:: 0.7
