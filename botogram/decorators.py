"""
    botogram.decorators
    Utility decorators used by the bot creators

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import utils


@utils.deprecated("@botogram.pass_bot", "1.0", "Just remove the decorator")
def pass_bot(func):
    """This decorator is deprecated, and it does nothing"""
    # What this decorator did is now done by default
    return func


@utils.deprecated("@botogram.pass_shared", "1.0", "Just remove the decorator")
def pass_shared(func):
    """This decorator is deprecated, and it does nothing"""
    # What this decorator did is now done by default
    return func


def help_message_for(func):
    """The return of the decorated function will be the help message of the
    function provided as an argument."""
    def decorator(help_func):
        func._botogram_help_message = help_func
        return help_func
    return decorator
