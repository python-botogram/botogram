.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _unavailable-chats:

==============================
Dealing with unavailable chats
==============================

Your bot can't send messages to everyone, because there are some restrictions
in place enforced by Telegram: you can't send messages to people who never
spoken with you before, people who blocked your bot and some more cases.

When you try to do that, botogram aborts the hook processing, and allows you to
react to that event: for example, if you're sending bulk messages to users and
one of them blocked your bot, you can remove it from the list of recipients.

.. versionadded:: 0.3

.. _unavailable-chats-reasons:

Possible reasons why a chat is not available
============================================

Here there is a list of the current reasons why a chat isn't available:

* **blocked**: the user blocked your bot, probably because he don't want to
  interact with your bot anymore.

* **account_deleted**: the user deleted his account, so you won't be able to
  send messages to him anymore.

* **chat_moved**: the chat was moved to a new ID. This currently happens if the
  group was converted into a supergroup.

* **not_found**: the chat ID you're trying to contact doesn't exist!

* **kicked**: your bot was kicked from the group chat you're trying to send
  messages to.


.. _unavailable-chats-react:

Take action when a chat isn't available
=======================================

Reacting to an unavailable chat is really easy in botogram: you just need to
decorate the function which will take action with the
:py:meth:`~botogram.Bot.chat_unavailable` decorator:

.. code-block:: python

   @bot.chat_unavailable
   def remove_user(chat_id, reason):
       # Remove the user from our database
       db_connection.query("DELETE FROM users WHERE id = ?", chat_id)

Keep in mind that your function will be called even if the message was sent
from a different component, so check if you're keeping track of that ID before
trying to delete it. The function will be supplied with two arguments:

* **chat_id**: the ID of the chat which you can't contact.

* **reason**: the reason why you can't contact the chat, as a string. You can
  see the list of all the possible reason in the :ref:`section above
  <unavailable-chats-reasons>`.

If you're writing a component, you can instead call the
:py:meth:`~botogram.Component.add_chat_unavailable_hook` method of your
component:

.. code-block:: python

   class RemoveUserComponent(botogram.Component):
       component_name = "remove-user"

       def __init__(self, db):
           self.db = db
           self.add_chat_unavailable_hook(self.remove_user)

       def remove_user(self, chat_id, reason):
           """Remove the user from the database"""
           self.db.query("DELETE FROM users WHERE id = ?", chat_id)

.. _unavailable-chats-catch:

Directly catch the exception while processing the update
========================================================

The global :py:meth:`~botogram.Bot.chat_unavailable` decorator is handy because
you don't have to deal with unavailable chats everytime you send a message. The
bad thing is, it aborts the update processing, so it's not suitable to use if
you're sending bulk messages to multiple users.

In those cases, you can directly catch the exception raised by botogram, so you
can take action without aborting the update processing:

.. code-block:: python

   @bot.command("send")
   def send_command(bot, chat, message, args):
       """Send a messages to a list of users"""
       message = " ".join(args)
       users = [12345, 67890, 54321]

       for user in users:
           try:
               bot.chat(user).send(message)
           except botogram.ChatUnavailableError as e:
               print("Can't send messages to %s (reason: %s)" %
                     (e.chat_id, e.reason))
               users.remove(user)
