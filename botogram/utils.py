"""
    botogram.utils
    Utilities used by the rest of the code

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


def format_docstr(docstring):
    """Prepare a docstring for /help"""
    result = []
    for line in docstring.split("\n"):
        stripped = line.strip()

        # Allow only a blank line
        if stripped == "" and len(result) and result[-1] == "":
            continue

        result.append(line.strip())

    # Remove empty lines at the end or at the start of the docstring
    for pos in 0, -1:
        if result[pos] == "":
            result.pop(pos)

    return "\n".join(result)


class HookDetails:
    """Container for some details of user-provided hooks"""

    def __init__(self, func):
        self._func = func
        self.name = ""
        self.component = None
        self.pass_bot = False
        self.help_message = None

    def _default_help_message(self):
        return format_docstring(self._func.__doc__)
