.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _custom-components:

==========================
Creating custom components
==========================

Hopefully you'll get to a point when you've made a few bots. The problem is,
there's a high chance parts of the code are duplicated between the bots. For
example, if your bots are meant to be used only by some people, you'll have
duplicate code which filters who can interact with the bot.

Components provide an easy and elegant way to solve the problem: instead of
copy-pasting the shared code in each bot, they allow you to create isolated
groups of hooks, commands and so on, then you can import and use them in each
bot.

.. _custom-components-conduct:

Components code of conduct
==========================

If you want to distribute your components, you should follow these simple rules
while coding them. This way all components will adhere to the same standards,
simplifying the end-user experience:

* **Give appropriate names to your components**. Naming your component
  appropriately will help users identify runtime actions involving your
  component, such as when the component is loaded into their bot, or if a hook
  defined by your component is called (when running in debug mode). Also, to
  be sure your component's name isn't used by someone else, consider adding
  your nickname as a prefix.

* **Don't assume your component will be used only by one bot**. Try to design
  your component in a way it can be used by multiple bots at once. This
  includes :ref:`requesting the bot instance <tricks-dynamic-arguments>` via
  arguments when you need it.

* **Store everything in the shared memory**. :ref:`Shared memory
  <shared-memory>` provides a simple way to store your component's data,
  synchronizes its content between multiple workers, and isolates automatically
  multiple bots.

* **Allow customizations both via the constructor and attributes**. Users
  should be able to use your bot the way they like, so you should allow them
  both to initialize the component with all the customizations, for a direct
  usage, and to initialize it without customizations, if they want to provide
  them later.

.. _custom-components-example:

An example component
====================

In this example we're going to write a simplified Access Control List component
called ``myacl``. That component will have an attribute containing the list of
allowed users, and only those will be allowed to communicate with the bot.

In order to be able to reuse the component in multiple bots, we'll write all
its code in the ``myacl.py`` file. Let's start by subclassing
:py:class:`botogram.Component` and giving the component the name we decided
before:

.. code-block:: python

   import botogram

   class MyACL(botogram.Component):
       component_name = "myacl"

Now we have a valid botogram component, even if it does nothing. The first
thing we should add is a list of users allowed to use the bot, customizable by
the end-user:

.. code-block:: python
   :emphasize-lines: 3,4,5,6

       component_name = "myacl"

       def __init__(self, allowed=None):
           if allowed is None:
               allowed = []
           self.allowed = allowed

And finally we can write the actual filter. We're going to use a
``before_processing`` filter, and to add it to the component we're going to use
the :py:meth:`botogram.Component.add_before_processing_hook` method:

.. code-block:: python
   :emphasize-lines: 2,3,4,5,6

           self.allowed = allowed
           self.add_before_processing_hook(self.filter)

       def filter(self, chat, message):
           if message.sender.id not in self.allowed:
               return True  # Stop processing the update

And the component is complete! The filter simply checks if the message
sender's ID is in the allowed list. If not, it tells botogram the message was
successfully processed, preventing the calls to all the other hooks. The full
source code of the component is the following:

.. code-block:: python

   import botogram

   class MyACL(botogram.Component):
       component_name = "myacl"

       def __init__(self, allowed=None):
           if allowed is None:
               allowed = []
           self.allowed = allowed
           self.add_before_processing_hook(self.filter)

       def filter(self, chat, message):
           if message.sender.id not in self.allowed:
               return True  # Stop processing the update

.. _custom-components-use:

Using a custom component
========================

If you want to use a component you created in your bots, you need to initialize
its object and apply it to each bot you want. We're going to apply the
``myacl`` component we wrote before, which should be in a separated file, to
the hello world bot you can find in the index of the docs:

.. code-block:: python

   import botogram
   bot = botogram.create("YOUR-API-KEY")

   @bot.command("hello")
   def hello_command(chat, message, args):
       """Say hello to the world!"""
       chat.send("Hello world")

   if __name__ == "__main__":
       bot.run()

First of all we need to import the component (located in the ``myacl.py`` file)
and configure it, creating an instance and putting someone in the allowed list:

.. code-block:: python
   :emphasize-lines: 2,3,4,5

   import botogram
   import myacl

   acl = myacl.MyACL()
   acl.allowed = [12345, 23456]

   bot = botogram.create("YOUR-API-KEY")

And finally we can tell the bot to use the component:

.. code-block:: python
   :emphasize-lines: 2

   bot = botogram.create("YOUR-API-KEY")
   bot.use(acl)

Now only the users with either the ``12345`` or ``23456`` IDs will be able to
chat with the bot. Mission accomplished!
