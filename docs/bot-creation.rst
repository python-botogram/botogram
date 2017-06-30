.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _bot-creation:

=========================
Create a new Telegram bot
=========================

Before you start writing any code, you should create your bot on Telegram. This
reserves your bot an username, and gives you the API key you need to control
your bot. This chapter explains you how to do so.

.. _bot-creation-naming:

Choose a good username for your bot
===================================

The username of your bot is really important: users will use it to tell their
friends about your bot, and it will appear on telegram.me links. Also, you're
not allowed to change username without recreating your bot, and so without
losing users.

Bot usernames must adhere to the following rules:

* The username must be long at least five characters
* The username can only contain letters, digits and underscores
* The username must end with ``bot``

For example, all the following usernames are valid: ``my_awesome_bot``,
``SpamBot``, ``test123bot``.

.. _bot-creation-botfather:

Create the bot with @botfather
==============================

Currently, you can only create a new bot... with another bot. With your
Telegram client open, contact `@botfather`_, start it and execute the
``/newbot`` command. It will ask you some questions about your bot.

Then it will give you an unique API key, which you can use to communicate with
your bot. **Be sure to keep this key secret!** Everyone with your API key can
take full control of your bot, and that's not a fun thing.

.. _bot-creation-customization:

Customize your bot
==================

Other than allowing you to create it, `@botfather`_ also permits you to
customize your bot. For example, you can use it to change your bot's avatar,
its name, or its description. In order to see what you can do, just use the
``/help`` command on @botfather. Then execute the command for the thing you
want to customize.

If you want to use your bot just to manage a channel, you probably don't need
to do this.

.. _@botfather: https://telegram.me/botfather
