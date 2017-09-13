.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _deploy-supervisor:

======================
Deploy with Supervisor
======================

Supervisor_ is a process management system written in Python, which allows you
to run applications in a controlled and reliable way. It features running
things in the background, rotation of the log files, and automatic restarts
of crashed applications.

Supervisor is the best choice for deploying botogram-powered bots, since it
provides a cross-distro, reliable and simple way to do that.

.. _deploy-supervisor-install:

Installation of Supervisor
==========================

Your distribution should have Supervisor in its repositories. On Debian/Ubuntu
you can install it with this command (from **root**)::

   $ apt-get install supervisor

Instead, on the CentOS/Fedora land, you need this command (from **root**)::

   $ yum install supervisor

And you're good to go! Refer to your distribution's documentation for more
information about this process.

.. _deploy-supervisor-install-pip:

Cross-distribution installation with pip
----------------------------------------

If your distribution hasn't a Supervisor package yet, or you need features
included in the latest release, you can install it from PyPI (from **root**)::

   $ python3 -m pip install supervisor

Then you can save the basic configuration file to its location with the
following command with this command (from **root**)::

   $ echo_supervisord_conf > /etc/supervisord.conf

Finally, you can start Supervisor with this command (from **root**)::

   $ supervisord -c /etc/supervisord.conf

It's advisable to automatically run Supervisor at boot with your distribution's
init process, which might vary from one distro to another. Refer to your
distribution's documentation for more information about adding a process to the
init system.

.. _deploy-supervisor-bot:

Preparation of the bot
======================

First thing to do is to create a user which will own the bot. This allows your
bot to run in isolation from other processes, increasing the security of your
deployment. The user will be called ``telegrambot`` (from **root**)::

   $ adduser telegrambot --disabled-password

You can safely leave empty the extra information ``adduser`` asks you. When
you've created the user you can log into it with ``su`` (from **root**)::

   $ su telegrambot

You're now in a shell as the user we created before. You should now decide
where you want your bot's files to be. We'll put them in the user's home
directory (``/home/telegrambot``).

Next thing to do is to create a virtual environment, which will contain the
botogram installation. After you've installed virtualenv in your server, you
can execute the following commands to create and activate it it::

   $ virtualenv -p python3 env
   $ source env/bin/activate

After you've activated the virtualenv, you can :ref:`install botogram
<install>` into it and exit with ``deactivate``. And finally place your bot's
source code in the home directory (we'll suppose it's located on ``mybot.py``).

.. _deploy-supervisor-config:

Creation of the bot's configuration file
========================================

Now it's time to tell Supervisor our bot exists. The following configuration
code should be appended to the Supervisor configuration file, which in a lot of
distributions is located at ``/etc/supervisord.conf``::

   [program:mybot]
   command=/home/telegrambot/env/bin/python3 /home/telegrambot/mybot.py
   directory=/home/telegrambot

   autostart=true
   autorestart=unexpected
   startsecs=5
   startretries=2

   stopsignal=INT
   stopwaitsecs=60

   user=telegrambot

   redirect_stderr=true
   stdout_logfile=/home/telegrambot/mybot.log
   stdout_logfile_maxbytes=10MB

This will create a process named ``mybot`` with some standard configuration:

1. Supervisor will execute the bot with the Python we have in the virtualenv.
2. The default directory will be the user's home directory.
3. The process will be started when Supervisor starts, and it will be restarted
   if it crashes.
4. The process will be run as ``telegrambot``.
5. All the output will be redirected in ``/home/telegrambot/mybot.log``.

You can refer to the `Supervisor documentation`_ for the reference of all the
configuration options.  Finally you can reload Supervisor's configuration to
get the process up and running (from **root**)::

   $ supervisorctl reread
   $ supervisorctl update

.. _deploy-supervisor-manage:

Managing the runner
===================

Wonderful, your bot is now up and running! You can control it with the
following commands (from **root**)::

   # Start the runner
   $ supervisorctl start mybot

   # Stop the runner
   $ supervisorctl stop mybot

   # Restart the runner
   $ supervisorctl restart mybot

.. _Supervisor: http://supervisord.org/
.. _Supervisor documentation: http://supervisord.org/configuration.html#program-x-section-settings
