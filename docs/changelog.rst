.. Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _changelog:

~~~~~~~~~~~~~~~~~~
botogram changelog
~~~~~~~~~~~~~~~~~~

Here you can see what changed in every botogram release.

.. _changelog-0.2:

botogram 0.2
=============

*Alpha release, not yet released*

* Renamed ``Bot.init_shared_memory`` to ``Bot.prepare_memory``
* Renamed ``Component.add_shared_memory_initializer`` to
  ``Component.add_memory_preparer``

The following things are now **deprecated**:

* ``Bot.init_shared_memory``, and it will be removed in botogram 1.0
* ``Component.add_shared_memory_initializer``, and it will be removed in
  botogram 1.0

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
