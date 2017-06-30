# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.


class Command:
    """Representation of a single command"""

    def __init__(self, hook, _bot=None):
        # Get some parameters from the hook
        self.name = hook._name
        self.hidden = hook._hidden
        self.order = hook._order

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
