.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _deploy-screen:

================================
Quick deployment with GNU screen
================================

`GNU screen`_ is an handy tool which lets you create shell sessions detached
from your current session. This means they will keep running even if you log
out from the server.  With it, you're able to run your bot in the exact same
way you're running it in your development machine, without worrying about
anything else.

.. warning::

   This deployment method is **not** recommended for real-world deployments,
   because it doesn't try to keep alive your bot if it crashes. It's explained
   here because this method is useful if you just want to test how the bot runs
   on the server.

The first thing you need to do is to install the tool. On Debian/Ubuntu you can
execute the following command (from **root**)::

   $ apt-get install screen

Instead, on CentOS/Fedora you need to run this command (from **root**)::

   $ yum install screen

Perfect, you now have GNU screen installed. You can create a new screen with
the following command (replace ``screen_name`` with the name you want to assign
to the screen)::

   $ screen -S screen_name

And you're into your screen. Now, :ref:`install botogram <install>` (if you
didn't do that before) and run your bot in it, as you would do on your local
machine. You can exit the screen anytime by pressing ``CTRL+A`` and then ``D``.
If you want to resume it later, run the following command::

   $ screen -x screen_name

Remember that if you don't enable the multiuser feature, you can't attach to
screens of other users, so be sure to be logged in with the same account as you
started the screen.

.. _GNU screen: https://www.gnu.org/software/screen/
