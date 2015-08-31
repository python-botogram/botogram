.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _api-components:

~~~~~~~~~~~~~~~~~~~~~~~
Components creation API
~~~~~~~~~~~~~~~~~~~~~~~

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
      custom component, be sure to set it to an appropiate value.

   .. py:method:: add_before_processing_hook(func)

      The function provided to this method will be called before an update is
      processed by a bot which uses the component. This allows you, for
      example, to set up a filter on who can send messages to the bot.
      Provided functions will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
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
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param callable func: The function you want to add.

   .. py:method:: add_message_contains_hook(string, func, [ignore_case=True, multiple=False])

      The function provided to this method will be called only if the
      processed message matches the ``string`` you provided. You may also
      define if you want to ignore the casing, and if the function should be
      called multiple times when multiple matches are found in the same
      message. Provided functions will be called with two parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param str string: The string you want contained in the message
      :param callable func: The function you want to use.
      :param bool ignore_case: If the match should be ignore-case
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:method:: add_message_matches_hook(func)

      The function provided to this method will be called only if the
      processed message matches the ``regex`` you provided. You may also
      pass the ``re`` module's flags, and if the function should be called when
      multiple matches are found in the same message. Provided functions will
      be called with three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * A ``matches`` parameter with a tuple containing the matched groups

      If the function returns ``True``, then the message processing is stopped,
      and no more functions will be called for that update.

      :param str string: The string you want contained in the message
      :param callable func: The function you want to use.
      :param int flags: ``re`` module's flags
      :param bool multiple: If the function should be called multiple times on
         multiple matches.

   .. py:method:: add_command(name, func)

      This function registers a new command, and calls the provided function
      when someone issues the command in a chat. The command will also be added
      to the ``/help`` message. The provided function will be called with
      three parameters:

      * A ``chat`` parameter with the representation of the chat in which the
        message was sent (either an instance of :py:class:`botogram.User` or
        :py:class:`botogram.GroupChat`)
      * A ``message`` parameter with the representation of the received
        message (an instance of :py:class:`botogram.Message`)
      * An ``args`` parameter with the list of parsed arguments

      If you put a docstring on the provided function, that will be used as
      extended description of the command in the ``/help`` command.

      .. note::

         Commands defined in custom components can be overridden by other
         components or by the bot developer.

      :param str name: The name of the command.
      :param callable func: The function you want to use.
