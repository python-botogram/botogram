.. Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _changelog:

==================
botogram changelog
==================

Here you can see what changed in every botogram release.

.. _changelog-0.2:

botogram 0.2
=============

*Alpha release, not yet released*

botogram 0.2 is the second alpha release of botogram. It features an increased
support for the upstream Telegram API, and also some bugfixes here and there.

This release also does some cleanup in the API, providing better methods and
deprecating the old ones. The deprecated methods will be available until
botogram 1.0, and warnings are in place to notify you where to change what.

New features
------------

* Added the :py:attr:`botogram.User.name` computed attribute
* Added the :py:attr:`botogram.Chat.name` computed attribute
* Added the :py:attr:`botogram.User.avatar` attribute
* Added the :py:meth:`botogram.User.avatar_history` method

Changes
-------

* Renamed ``Bot.init_shared_memory`` to :py:meth:`botogram.Bot.prepare_memory`
* Renamed ``Component.add_shared_memory_initializer`` to
  :py:meth:`botogram.Component.add_memory_preparer`

Bug fixes
---------

* Fix the syntax detector checking URLs with dashes in the domain (`issue 32`_)
* Fix inability to send messages to channels from a running bot (`issue 35`_)

Deprecated features
-------------------

Deprecated features will be removed in botogram 1.0!

* ``Bot.init_shared_memory`` is now deprecated
* ``Component.add_shared_memory_initializer`` is now deprecated

.. _issue 32: https://github.com/pietroalbini/botogram/issues/32
.. _issue 35: https://github.com/pietroalbini/botogram/issues/35

.. _changelog-0.1.2:

botogram 0.1.2
==============

*Bugfix release, released on February 25th, 2016*

* Add a way to disable the syntax detector (`issue 27`_)
* Fix automatic syntax detector recognizing markdown in URLs (`issue 28`_)

.. _issue 27: https://github.com/pietroalbini/botogram/issues/27
.. _issue 28: https://github.com/pietroalbini/botogram/issues/28

.. _changelog-0.1.1:

botogram 0.1.1
==============

*Bugfix release, released on February 21th, 2016*

* Fix automatic syntax detector not working sometimes (`issue 26`_)
* Fix "unknown command" message not showing up in private chats (`issue 25`_)

.. _issue 25: https://github.com/pietroalbini/botogram/issues/25
.. _issue 26: https://github.com/pietroalbini/botogram/issues/26

.. _changelog-0.1:

botogram 0.1
============

*Alpha release, released on February 18th, 2016*

This is the initial alpha release of botogram.
