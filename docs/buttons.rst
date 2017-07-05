.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _buttons:

=====================
Buttons and callbacks
=====================

Buttons are a really powerful way to construct user interfaces: they allows you
to attach multiple rows of buttons under a single message, and when the user
presses them it can trigger callbacks on your bot.

Be sure to also :ref:`check out the API documentation <api-buttons>` for this
feature.

.. versionadded:: 0.4

.. _buttons-intro:

Creating your first message with buttons
----------------------------------------

Let's create a simple bot that sends a message that can be deleted by the user
if a button is clicked. While it's almost useless in a real bot, it explains
better how this works.

First of all we need a command that sends the message. We'll call this command
``/spam``:

.. code-block:: python

   @bot.command("spam")
   def spam_command(chat, message, args):
       """Send a spam message to this chat"""
       btns = botogram.Buttons()
       btns[0].callback("Delete this message", "delete")

       chat.send("This is spam!", attach=btns)

There is a lot going on in this simple example. Let's break it down!

First of all, we defined a new command called ``/spam``, as we would normally
do. Then we created an instance of :py:class:`~botogram.Buttons`, which allows
us to define which buttons should be sent to the user. We only have one button,
labelled "Delete this message". This button is located in the first row, and
when the user clicks on it the ``delete`` callback will be executed by the bot.
Finally, we send the spam message to the user, attaching to it the buttons.

This command already works: when the user calls it, the message with the
buttons will be sent, and the user can click on them. Unfortunately, clicking
the button will do nothing, because we haven't created the callback yet! Let's
create it:

.. code-block:: python

   @bot.callback("delete")
   def delete_callback(query, chat, message):
       message.delete()
       query.notify("Spam message deleted. Sorry!")

This piece of code registers a new callback called ``delete``, and deletes the
messages attached to the button that triggered the callback. It also notifies
the user that the message was deleted. The appearance of the notification
depends on the user's client.

Your bot is now complete! Here is the full code if you want to try it:

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-TOKEN")

   @bot.command("spam")
   def spam_command(chat, message, args):
       """Send a spam message to this chat"""
       btns = botogram.Buttons()
       btns[0].callback("Delete this message", "delete")

       chat.send("This is spam!", attach=btns)

   @bot.callback("delete")
   def delete_callback(query, chat, message):
       message.delete()
       query.notify("Spam message deleted. Sorry!")

   if __name__ == "__main__":
       bot.run()

.. _buttons-callback-data:

Passing data to callbacks
-------------------------

Sometimes, you might need some data in the callbacks that you only have when
you're creating the button. For example, if you have a callback to unban an
user from a group you need to provide to it the user ID.

Telegram allow you to do so, but with a limitation: you can provide a maximum
of 32 bytes of string as the data (which means 32 characters if you use only
ASCII chars). If you can't fit your data in it, it's advised to put that data
in a database and pass to the callback the ID of the row.

Let's create another bot, that asks the user how it feels. We start by creating
a ``/survey`` command, similar to the one we created before.

.. code-block:: python

   @bot.command("survey")
   def survey_command(chat, message, args):
       """Reply to a simple survey!"""
       btns = botogram.Buttons()
       btns[0].callback("Great", "notify", "Happy to hear that!")
       btns[1].callback("Not so great", "notify", "I'm sorry! What happened?")

       chat.send("How are you feeling?", attach=btns)

The difference between the previous example and this one is the third argument
of the callback method: that's the data that will be provided to the callback!
In this case, the callback will receive the message it needs to send to the
user. Let's create it then:

.. code-block:: python

   @bot.callback("notify")
   def notify_callback(query, data, chat, message):
       query.notify(data)

This callback requires an additional parameter, ``data``, which contains the
information we provided before. In this simple callback we then notify the user
with that data.

This example now works as expected! Here is its source code:

.. code-block:: python

   import botogram

   bot = botogram.create("YOUR-TOKEN")

   @bot.command("survey")
   def survey_command(chat, message, args):
       """Reply to a simple survey!"""
       btns = botogram.Buttons()
       btns[0].callback("Great", "notify", "Happy to hear that!")
       btns[1].callback("Not so great", "notify", "I'm sorry! What happened?")

       chat.send("How are you feeling?", attach=btns)

   @bot.callback("notify")
   def notify_callback(query, data, chat, message):
       query.notify(data)

   if __name__ == "__main__":
       bot.run()

.. _buttons-other-types:

Other types of buttons
----------------------

Telegram doesn't support only callback buttons: it allows you to also define
buttons to open URLs in the user's browser, and to switch the user to the
inline query mode of your bot. You can add them as you would do with callbacks:

.. code-block:: python

   btns = botogram.Buttons()
   btns[0].url("Open an example", "http://example.com")
   btns[1].switch_inline_query("Use me as an inline bot!", "default query")

Check out the :py:class:`~botogram.Buttons` class for the documentation about
all the available methods.

.. _buttons-components:

Using buttons with components
-----------------------------

You can also use buttons and callbacks with :ref:`components
<custom-components>`: you can create and send buttons as you would normally do,
and you can add new callbacks with the
:py:meth:`~botogram.Component.add_callback` method of your component. Here is
the first example converted into a component:

.. code-block:: python

   class SpamComponent(botogram.Component):
       component_name = "spam"

       def __init__(self):
           self.add_command("spam", self.spam_command)
           self.add_callback("delete", self.delete_callback)

      def spam_command(self, chat, message, args):
          """Send a spam message to this chat"""
          btns = botogram.Buttons()
          btns[0].callback("Delete this message", "delete")

          chat.send("This is spam!", attach=btns)

      def delete_callback(self, query, chat, message):
          message.delete()
          query.notify("Spam message deleted. Sorry!")

One advantage of using components is that callback names lives in a different
namespace for every component: you can use any name without fearing to have
name clashes with other components or the main bot!

.. _buttons-security:

The security of callbacks
-------------------------

Unfortunately, callbacks are sent by the client, not by Telegram. This means a
malicious user can manipulate them (with a modified client), causing unexpected
behaviors.

While this might not matter too much if you have callbacks like "go back", it
might be dangerous if you assume all callbacks are authentic and you have
something like "delete message" with the ID of the message to delete as the
data, because the user can delete any message sent by the bot.

botogram mitigates this risk by digitally signing all the outgoing callbacks,
and rejecting all the incoming ones without a valid signature. This means even
if the user manages to change the content of the callback, the modified one
will be discarded.

Other than rejecting modified callbacks, botogram ties them to the chat they
were sent in: an incoming callback is discarded if it comes from a different
chat.

This protection is completly transparent: you don't have to do anything to
enable or manage it. The signature is based on the token of the bot though:
this means if you revoke or change the token, all previous callbacks will
become invalid, which may annoy your users because old buttons stop working.

If you want to avoid disruption after changing your bot's token, it's advised
to disable signature verification for a few days: it lowers the security of
your bot, but allows the user to keep using buttons under old messages. In
order to disable the verification you need to add this snippet of code before
the bot is started:

.. code-block:: python

   bot.validate_callback_signatures = False

You should remove the snippet after a few days. The bot will print a
warning at startup to remember you to do so.
