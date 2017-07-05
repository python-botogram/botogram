.. Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
   Documentation released under the MIT license (see LICENSE)

.. _api-components:

=======================
Components creation API
=======================

Creating components is one of the most useful features of botogram, since they
allows you to reuse parts of your code in multiple bots. You can learn more
about how to create them in the ":ref:`custom-components`" chapter.


.. py:class:: botogram.Component(name)

   This class contains all the information about your component. You can either
   create an instance of it (providing a name), or subclass the class if you
   want your custom component to be instanceable. In the latter case, you don't
   need to call the parent's init method, and you can remove the ``name``
   argument.

   You can get more information about how to create components in the
   ":ref:`custom-components`" chapter.

   :param str name: The name of the component.

   .. py:attribute:: component_name

      The name of the component. If you subclass the class in order to create a
      custom component, be sure to set it to an appropriate value.

   .. py:method:: add_before_processing_hook(func)

      The function provided to this method will be called before an update is
      processed by a bot which uses the component. This allows you, for
      example, to set up a filter on who can send messages to the bot.
      Provided functions will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param callable func: The function you want to add.

   .. py:method:: add_process_message_hook(func)

      The function provided to this method will be called while processing an
      update. You can then do everything you want in it. Provided functions
      will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param callable func: The function you want to add.

   .. py:method:: add_message_equals_hook(string, func, [ignore_case=True])

      The function provided to this method will be called only if the processed
      message is equal to the ``string`` you provided. You may also define if
      you want to ignore the casing. Provided functions will be called with two
      parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`).

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param str string: The string you want equals to the message
      :param callable func: The function you want to use.
      :param bool ignore_case: If the check should be ignore-case

   .. py:method:: add_message_contains_hook(string, func, [ignore_case=True, multiple=False])

      The function provided to this method will be called only if the
      processed message matches the ``string`` you provided. You may also
      define if you want to ignore the casing, and if the function should be
      called multiple times when multiple matches are found in the same
      message. Provided functions will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param str string: The string you want contained in the message
      :param callable func: The function you want to use.
      :param bool ignore_case: If the match should be ignore-case
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:method:: add_message_matches_hook(regex, func, [flags=0, multiple=False])

      The function provided to this method will be called only if the
      processed message matches the ``regex`` you provided. You may also
      pass the ``re`` module's flags, and if the function should be called when
      multiple matches are found in the same message. Provided functions will
      be called with three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * A ``matches`` parameter with a tuple containing the matched groups

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param str regex: The regular expression the message should match
      :param callable func: The function you want to use.
      :param int flags: ``re`` module's flags
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:method:: add_message_edited_hook(func)

      All the functions provided to this method will be called when an user
      edits a message the bot knows about. This allows you, for example, to
      update the preview of a message if the user edits the request, or to
      enforce a no-edits policy on groups by banning whoever edits a message.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the provided functions:

      * **chat**: the chat in which the message was orignally sent (instance of
        :py:class:`~botogram.Chat`)
      * **message**: the edited message (instance of
        :py:class:`~botogram.Message`)

      .. code-block:: python

         class NoEditsComponent(botogram.Component):
             component_name = "noedits"

             def __init__(self):
                 self.add_message_edited_hook(self.no_edits)

             def no_edits(self, chat, message):
                 message.reply("You can't edit messages! Bye.")
                 chat.ban(message.sender)

      :param callable func: The function you want to use.

      .. versionadded:: 0.3

   .. py:method:: add_channel_post_hook(func)

      All the functions provided to this method will receive all the messages
      posted to channels the bot is a member of. This allows you to act when
      certain messages are received, as an example.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the provided functions:

      * **chat**: the chat in which the channel post was originally sent
        (instance of :py:class:`~botogram.Chat`)

      * **message**: the message (instance of :py:class:`~botogram.Message`)

      .. code-block:: python

         class ChannelAckComponent(botogram.Component):
             component_name = "channel-ack"

             def __init__(self):
                 self.add_channel_post_hook(self.reply)

            def reply(self, chat, message):
                message.reply("I read this post!")

      :param callable func: The function you want to use.

      .. versionadded:: 0.4

   .. py:method:: add_channel_post_edited_hook(func)

      All the functions provided to this method will receive all the messages
      edited in channels the bot is a member of. This allows you to act when
      certain messages are changed, as an example.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the provided functions:

      * **chat**: the chat in which the channel post was originally sent
        (instance of :py:class:`~botogram.Chat`)

      * **message**: the (new) edited message (instance of :py:class:`~botogram.Message`)

      .. code-block:: python

         class ChannelAlertComponent(botogram.Component):
             component_name = "channel-alert"

             def __init__(self):
                 self.add_channel_post_edited_hook(self.reply)

            def reply(self, chat, message):
                message.reply("This post is changed!")

      :param callable func: The function you want to use.

      .. versionadded:: 0.4

   .. py:method:: add_command(name, func, [hidden=False, order=0])

      This function registers a new command, and calls the provided function
      when someone issues the command in a chat. The command will also be added
      to the ``/help`` message. The provided function will be called with
      three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (an instance of :py:class:`botogram.Chat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * An ``args`` parameter with the list of parsed arguments

      If you put a docstring on the provided function, that will be used as
      extended description of the command in the ``/help`` command.

      Also, if you don't want this command to appear in the ``/help``, you can
      set the ``hidden`` argument to ``True``.

      .. note::

         Commands defined in custom components can be overridden by other
         components or by the bot developer.

      :param str name: The name of the command.
      :param callable func: The function you want to use.
      :param bool hidden: If the command should be hidden from ``/help``
      :param int order: The order in which the commands are shown in ``/help``

      .. versionchanged:: 0.4

         Added the ``order`` argument.

      .. versionchanged:: 0.3

         Added the ``hidden`` argument.

   .. py:method:: add_callback(name, func)

      This method adds an handler for the callback with the provided name.
      See the chapter about :ref:`buttons and callbacks <buttons>` for more
      information about them.

      You can :ref:`request the following arguments <bot-structure-hooks-args>`
      in the provided function:

      * **query**: the received :py:class:`~botogram.CallbackQuery`

      * **chat**: the :py:class:`~botogram.Chat` from which the callback query
        was sent

      * **message**: the :py:class:`~botogram.Message` related to the callback
        query

      * **data**: the custom information provided by you along with the call

      .. code-block:: python

         class GreeterComponent(botogram.Component):
             component_name = "greeter"

             def __init__(self):
                 self.add_command("greeter", self.command)
                 self.add_callback("say-hi", self.say_hi)

             def greeter(self, chat, message):
                 """Say hi to the user"""
                 btns = botogram.Buttons()
                 btns[0].callback("Click me", "say-hi", message.sender.name)

                 chat.send("Click the button below", attach=btns)

             def say_hi(self, query, data):
                 query.notify("Hi " + data)

      :param str name: the name of the callback
      :param callable func: The function you want to use

      .. versionadded:: 0.4

   .. py:method:: add_chat_unavailable_hook(func)

      The provided function is called when you try to send a message to a chat
      you can't send messages to. There are currently multiple reasons why that
      can happen, and you can see all of them :ref:`in the narrative
      documentation <unavailable-chats-reasons>`.

      The provided function will be called with the following parameters:

      * **chat_id**: the ID of the chat which you can’t contact.
      * **reason**: the reason why you can’t contact the chat, as a string.

      If you want to learn more about unavailable chats check out :ref:`their
      documentation <unavailable-chats>`.

      :param callable func: The function you want to use.

   .. py:method:: add_timer(interval, func)

      Execute the provided function periodically, at the provided interval,
      which must be in seconds. You can learn more in the :ref:`tasks-repeated`
      section of the docs.

      .. code-block:: python

         class SpammerComponent:

             component_name = "spammer"

             def __init__(self, user_id=None, message="Hey!"):
                 self.user_id = user_id
                 self.message = message

                 self.add_timer(1, self.spam)

             def spam(self, bot):
                 bot.send(self.user_id, self.message)

      :param int interval: The execution interval, in seconds.
      :param callable func: The function you want to use.

   .. py:method:: add_memory_preparer(func)

      The function provided to this method will be called the first time you
      access your component's shared memory. This allows you to set the initial
      state of the memory, without having to put initialization code in every
      function which uses the shared memory. Please don't use this function as
      a "when the component is added to a bot" hook, because it's not
      guaranteed to be called if you don't use shared memory in all of your
      hooks.

      The provided function will be called providing as first argument a
      dict-like object representing your bot's shared memory. Use it to
      initialize the things you want in the shared memory.

      .. code-block:: python

         class CountComponent(botogram.Component):

             component_name = "counter"

             def __init__(self):
                 self.add_memory_preparer(self.initialize)
                 self.add_process_message_hook(self.increment)
                 self.add_command("count", self.count)

             def initialize(self, shared):
                 shared["messages"] = 0

             def increment(self, shared, chat, message):
                 if message.text is None:
                     return
                 shared["messages"] += 1

             def count(self, shared, chat, message, args):
                 chat.send("This bot received %s messages" % shared["messages"])

      .. versionchanged:: 0.2

         Before it was called ``add_shared_memory_initializer``.

   .. py:method:: add_shared_memory_initializer(func)

      This method was renamed to
      :py:meth:`~botogram.Component.add_memory_preparer` in botogram 0.2.
      Please use that instead of this.

      .. deprecated:: 0.2 it will be removed in botogram 1.0
