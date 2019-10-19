.. Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
Documentation released under the MIT license (see LICENSE)

.. _inline:

===========
Inline mode
===========

Inline bots make it possible to use bot services in any chat without adding those bots as members – you just  any message with their username and everything that comes after becomes a query for the bot.

To enable the Inline Mode on your bot you need to go to `BotFather <https://t.me/BotFather>`_ and write ``/mybots`` in the chat with him, then select your bot of choice, click ``Bot settings``, click on the button that says ``inline_mode``, then click ``turn_on``. Perfect, now you have ``inline_mode`` enabled on your bot ;-).

.. _BotFather https://t.me/BotFather

Create your first reply inline
------------------------------
Let's create a simple bot and create a hook

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
      yield inline.article("Hello World",botogram.InlineInputMessage("Hello World message"))

Inline Processor needs to process all the articles of the inline. In this small example you can see an Hello World message that is send when the Hello World article is clicked. :py:meth:`~botogram.inline.InlineQuery.article`

How paginate works and what is it for
-------------------------------------

.. code-block:: python

  @bot.inline(paginate=10)
  def inline_processor(inline):
      for i in range(100):
         if i == 20:
             inline.paginate = 20
         yield inline.article("Hello World "+ str(i),botogram.InlineInputMessage("Hello World message "+str(i)))

In this example you can see an evolution of the precedent code. The ``paginate`` parameter needs to decide how many messages to send to Telegram (**ATTENTION: it is not recommended to use paginate under 5**). This is required not to overload the system of unnecessary request. The system of ``paginate`` is managed by Botogram Core and can be edited locally with "``inline.paginate = int``" and globally with ``@bot.inline(paginate=int)``.

Work with queries
---------------

Now you will see how to work with queries

.. code-block:: python

  @bot.inline
  def inline_processor(inline,query):
    if query is "hello":
      yield inline.article("Hello World",botogram.InlineInputMessage("Hello World message"))
    else:
      yield inline.article("Write hello",botogram.InlineInputMessage("Write hello in inline mode"))

In this example you can see what ``Inline Query`` is and how it works. To use ``query`` you can use two methods, the first is to ask a query argument ``inline_processor``, the second method is to use ``"query = inline.query"``.
The ``query`` is the text written after the bot username.

Work with buttons
-----------------

.. code-block:: python

  @bot.inline
  def inline_processor(inline):
    btns = botogram.buttons()
    btns[0].url("botogram docs", "https://botogram.dev/")
    btns[0].callback("text of message", "button")
    yield inline.article("Hello World",botogram.InlineInputMessage("Hello World message"),attach=btns)

    message.is_inline
  @bot.callback("button")
  def button_callback(message):
      message.edit("edit message")

In this example you can see how buttons works with ``Inline Mode``, plus some differences compared to non-inline buttons. Some differences are: ``message.date`` returns ``None``, ``message.chat`` returns ``None``, now it exists a new parameter, ``message.is_inline`` (Returns True if it is from an inline message, else it returns False), ``message.id`` returns the id of the inline message (**the reply function does not work with the inline mode**)

In this example code you can see how the buttons in the ``Inline Mode`` works. You can see that it changes a little from non-inline buttons, the only difference is that the chat parameter in callback is none.

How buttons.switch_inline_query() works
------------------------------------------

.. code-block:: python

    @bot.inline
  def inline_processor(inline):
    btns = botogram.buttons()
    btns[0].url("botogram docs", "https://botogram.dev/")
    yield inline.article("Hello World",botogram.InlineInputMessage("Hello World message"),attach=btns)


  @bot.command("start")
  def button_callback(chat):
      btns = botogram.buttons()
      btns[0].switch_inline_query("test me", current_chat=True)
      chat.send("click the button qui sotto", attach=btns)

In questo esempio vedremo il funzionamento

In this example we will see how [coso] funziona

.. versionadded:: 0.7
