.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _groups-management:

======================
Moderating group chats
======================

Group chats are an awesome way to communicate with your circle of friends, but
you can also use them to discuss with other users in public groups.
Unfortunately, there are people who just want to spam their own groups or post
inappropriate content and, without some moderators always online, a public
group will get messy sooner or later.

Telegram bots are able to moderate groups easily, so you can programmatically
ban and unban users of the groups your bot is an administrator of.

.. versionadded:: 0.3

.. _groups-management-preparation:

Allowing your bot to moderate groups
====================================

Bots can't moderate groups by default, but they need to be authorized to do so.
How to authorize them is specific to the client you use, but take the following
advices:

* If you're trying to add your bot as administrator to a **group**, you need to
  disable the "Everyone is an admin" setting of it, and then explicitly mark
  your bot as administrator.

* If you're trying to add your bot as administrator to a **supergroup**, just
  add it to the administrators list.

Keep in mind your bot might lose its status of administrator during the
conversion from a group to a supergroup, so if you converted a group check if
your bot is still an administrator of it.

.. _groups-management-ban:

Banning nasty users
===================

Nobody wants users joining a public groups just to spam their own group but, if
there isn't a moderator always online, a spammer can join in the middle of the
night, and multiple users might see their message before a moderator gets
online to ban him.

As an example, with the aid of :py:class:`~botogram.ParsedText` you can detect
all the posted URLs, and ban all the user who sends a ``telegram.me`` link,
with :py:meth:`botogram.Chat.ban`. Unfortunately bots can't delete messages
yet, but they can mention all the administrators of the group, so they can
erase that message later:

.. code-block:: python
   :emphasize-lines: 15,16

   @bot.process_message
   def ban_telegram_links(chat, message):
       # Don't do anything if there is no text message
       if message.text is None:
           return

       # Check all the links in the message
       for link in message.parsed_text.filter("link"):
           # Match both HTTP and HTTPS links
           if "://telegram.me" in link.url:
               break
       else:
           return

       # Ban the sender of the message
       chat.ban(message.sender)

       # Tell all the admins of the chat to delete the message
       admins = " ".join("@"+a.username for a in chat.admins if a.username)
       if admins:
           message.reply("%s! Please delete this message!" % admins)
       return

.. _groups-management-unban:

Unbanning users from supergroups
================================

If an user is banned from a group chat, he can rejoin the group if he uses a
join link or it's added by another member. Instead, when an user is banned from
a supergroup he's put in a blacklist, and he needs to be explicitly removed
from it if he want to join the supergroup again.

The following example is a working tempban code, which stores when the user was
banned in :ref:`the shared memory <shared-memory>`, with a :ref:`timer
<tasks-repeated>` to unban the user later. The actual unban is executed via the
:py:meth:`botogram.Chat.unban` method:

.. code-block:: python
   :emphasize-lines: 60

   import time

   # This means `/tempban 1` bans the user for 60 seconds
   BAN_DURATION_MULTIPLIER = 60

   @bot.prepare_memory
   def prepare_memory(shared):
       shared["bans"] = {}

   @bot.command("tempban")
   def tempban_command(shared, chat, message, args):
       """Tempban an user from the group"""
       # Handle some possible errors
       if message.sender not in chat.admins:
           message.reply("You're not an admin of this chat!")
           return
       if not message.reply_to_message:
           message.reply("You must reply to a message the user sent!")
           return
       if message.reply_to_message.sender in chat.admins:
           message.reply("You can't ban another admin!")
           return

       # Get the exact ban duration
       try:
           length = int(args[0])
       except (IndexError, TypeError):
           message.reply("You must provide the length of the ban!")
           return

       # Store the ban in the shared memory
       with shared.lock("bans-change"):
           bans = shared["bans"]
           if chat.id not in bans:
               bans[chat.id] = {}

           # Calculate the expiry time and store it
           expiry = time.time()+length*BAN_DURATION_MULTIPLIER
           bans[chat.id][message.reply_to_message.sender.id] = expiry
           shared["bans"] = bans

       # Let's finally ban this guy!
       chat.ban(message.reply_to_message.sender)

   @bot.timer(BAN_DURATION_MULTIPLIER)
   def unban_timer(bot, shared):
       """Unban the users"""
       now = time.time()

       # Everything is locked so no there are no races
       with shared.lock("bans-change"):
           global_bans = shared["bans"]

           # Here .copy() is used because we're changing the dicts in-place
           for chat_id, bans in global_bans.copy().items():
               for user, expires in bans.copy().items():
                   # Unban the user if his ban expired
                   if expires <= now:
                       continue
                   bot.chat(chat_id).unban(user)
                   del global_bans[chat_id][user]

               # Cleaning up is not such a bad thing...
               if not global_bans[chat_id]:
                   del global_bans[chat_id]

           shared["bans"] = global_bans
