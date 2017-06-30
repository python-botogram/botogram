.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _shared-memory:

===============================
Sharing objects between workers
===============================

botogram's runner is fast because it's able to process multiple messages at
once, and to archive this result botogram spawns multiple processes, called
"workers". The problem with this is, you can't easily share objects between the
workers, because each one lives in a different process, within a different
memory space.

The solution to this problem is shared memory. Shared memory allows you to
store global state without worrying about synchronizing it. It just works as a
standard Python dictionary. Also, each component has a different shared memory
than your bot, so you don't need to worry about conflicts between components.

.. _shared-memory-basics:

How to use shared memory
========================

If your function requires the ``shared`` argument, botogram will fill it
with your bot's shared memory object, which has the same API as the builtin
``dict``. Then, you can store in it everything you want, and it will be
synchronized between the processes.

Please note that the shared memory object is provided only if the function is
called by botogram itself: if you call it directly, that argument won't be
provided.

.. note::

   Synchronization uses pickle under the hood, so you can store in the shared
   memory only objects pickle knows how to serialize. Please refer to the
   official Python documentation for more information about this.

Here there is a simple example of an hook which uses the shared memory to count
how much messages has been sent:

.. code-block:: python

   @bot.process_message
   def increment(shared, chat, message):
       if "messages" not in shared:
           shared["messages"] = 0

       if message.text is None:
           return
       shared["messages"] += 1

As you can see, first of all the code initializes the ``messages`` key if it
doesn't exist yet. Then it just increments it. Next there is an example of a
command which displays the current messages count calculated by the hook above:

.. code-block:: python

   @bot.command("count")
   def count(shared, chat, message, args):
       messages = 0
       if "messages" in shared:
           messages = shared["messages"]

       chat.send("This bot received %s messages" % shared["messages"])

.. _shared-memory-inits:

Shared memory preparers
=======================

In the example above, a big part of the code is just to handle the case when
the shared memory doesn't contain the ``count`` key, and that's possible only
at startup. In order to solve this problem, you can use the
:py:meth:`~botogram.Bot.prepare_memory` decorator.

Functions decorated with that decorator will be called only the first time you
require the shared memory. This means you can use them to set the initial value
of all the keys you want to use in the shared memory.

For example, let's refactor the code above to use a preparer:

.. code-block:: python

   @bot.prepare_memory
   def prepare_memory(shared):
       shared["messages"] = 0

   @bot.process_message
   def increment(shared, chat, message):
       if message.text is None:
           return
       shared["messages"] += 1

   @bot.command("count")
   def count_command(shared, chat, message, args):
       chat.send("This bot received %s messages" % shared["messages"])

As you can see, the code is now clearer, and we can be sure the key we need
will always exist. This can especially be useful if you have a lot more hooks.

.. _shared-memory-components:

Shared memory in components
===========================

Shared memory is really useful while you're developing :ref:`components
<custom-components>`, because it's unique both to your component and the
current bot. This means, you don't have to worry about naming conflicts with
other components, and each bot's data will be isolated from each other if the
component is used by multiple bots.

Using shared memory within a component is the same as using it in your bot's
main code: just require the ``shared`` argument to your component's function
and botogram will make sure it receives the component's shared memories. To
add a shared memory preparer, you can instead provide the function to the
:py:meth:`~botogram.Component.add_memory_preparer` method.

.. _shared-memory-locks:

Dealing with concurrency issues with locks
==========================================

Normally you don't need to worry about concurrency issues in botogram:
everything is local to your process, and you can't interact with the other
ones. But when you start dealing with shared memory this isn't true anymore,
because two processes can write to the same key at the same time.

If you need to protect yourself from concurrency issues, shared memory's locks
are the way to go. They've the same API as the Python native ones, but they're
also customized to fit better in botogram.

In order to use locks you can call the ``lock`` method on a shared memories
object, providing to it the name of the lock. Then you can use it as a context
manager in order to lock specific parts of your code:

.. code-block:: python

   @bot.command("count")
   def count_command(shared, chat):
       """Send the number of messages sent in this chat"""
       chat.send("Number of messages: %s" % shared["messages"][chat.id])

   @bot.process_message
   def increment(shared, chat):
       """Example command for locks"""
       with shared.lock("update-messages"):
           messages = shared["messages"]
           messages[chat.id] += 1
           shared["messages"] = messages

Remember that lock names are unique to your bot/component, so you don't need to
worry about naming conflicts.
