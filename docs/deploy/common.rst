.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _deploy-common:

=============================
Common deployment information
=============================

Even if different deployment techniques are *really* different, all of them
have two essential things in common: server security and application
configuration.

.. _deploy-common-security:

Server security considerations
==============================

In a perfect world, you wouldn't need to worry about securing your servers,
because no one would attempt to break them. Unfortunately, we don't live in
that world, so you need to protect your server from the ones who love breaking
others' things.

* **You need to have experience in servers management**. Servers aren't easy to
  configure (especially if you want to do it in a secure way) and maintain: be
  sure to know how to do that before diving into servers management. It's the
  wild west out there.

* **Never run anything from root**. Even if (hopefully)
  there are no security vulnerabilities in botogram, it's always better to run
  any service from another user. This way if a service is compromised the
  attacker won't be able to do too much damage on your system.

* **Keeping services separated is a good idea**. In order to restrict even more
  what an hypothetical attacker can do, you can create a separate user for
  *each* service you have on your server. This way an attacker can't even
  compromise other applications.

* **Restrict what services can do**. Allowing a bot to
  SSH other servers isn't a good idea, right? botogram by default only needs to
  communicate to ``api.telegram.org`` with HTTPS. You can block everything else
  your bot doesn't use.

.. _deploy-common-multiple:

Running multiple bots in the same process
=========================================

A botogram runner uses system resources, even if the bot is doing nothing. With
only one bot this isn't a problem, but if you have a lot of small bots with low
traffic (for example bots only for a single group chat) this might become
annoying.

The solution is to run multiple bots in a single runner, since adding bots to a
runner is way more inexpensive than creating a runner per bot. Be warned
that if you add too many bots to a single runner, the workers might not be able
to keep up with the incoming requests.

In order to make this happen, you need to have each bot in an importable
Python file, and then create a file which calls :py:func:`botogram.run` with
the bots' instances. For example, if you have two bots in ``mybot1.py`` and
``mybot2.py``, and the bot instance in all of them is called ``bot``, you can
use this script to run both of them in a single runner:

.. code-block:: python

   import botogram
   from mybot1 import bot as bot1
   from mybot2 import bot as bot2

   if __name__ == "__main__":
       botogram.run(bot1.bot, bot2.bot)
