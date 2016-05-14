"""
    botogram.commands
    Core logic for commands

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


class Command:
    """Representation of a single command"""

    def __init__(self, hook, _bot=None):
        # Get some parameters from the hook
        self.name = hook._name
        self.hidden = hook._hidden

        self._hook = hook
        self._component_id = hook.component_id

        self._bot = _bot

    def __reduce__(self):
        return rebuild_command, (self._hook,)

    def for_bot(self, bot):
        """Get the command instance for a specific bot"""
        return self.__class__(self._hook, _bot=bot)

    @property
    def raw_docstring(self):
        """Get the raw docstring of this command"""
        func = self._hook.func

        if hasattr(func, "_botogram_help_message"):
            if self._bot is not None:
                return self._bot._call(func._botogram_help_message,
                                       self._component_id)
            else:
                return func._botogram_help_message()
        elif func.__doc__:
            return func.__doc__

        return

    @property
    def docstring(self):
        """Get the docstring of this command"""
        docstring = self.raw_docstring
        if docstring is None:
            return

        result = []
        for line in self.raw_docstring.split("\n"):
            # Remove leading whitespaces
            line = line.strip()

            # Allow only a single blackline
            if line == "" and len(result) and result[-1] == "":
                continue

            result.append(line)

        # Remove empty lines at the end or at the start of the docstring
        for pos in 0, -1:
            if result[pos] == "":
                result.pop(pos)

        return "\n".join(result)

    @property
    def summary(self):
        """Get a summary of the command"""
        docstring = self.docstring
        if docstring is None:
            return

        return docstring.split("\n", 1)[0]


def rebuild_command(hook):
    """Rebuild a Command after being pickled"""
    return Command(hook)
