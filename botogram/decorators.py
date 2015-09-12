"""
    botogram.decorators
    Utility decorators used by the bot creators

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import utils


def pass_bot(func):
    """An handy decorator which passes the current bot as first argument.

    Please note that the bot is passed only if the function is called by the
    bot itself, for example in an hook."""
    if not hasattr(func, "botogram"):
        func.botogram = utils.HookDetails(func)

    if id(func) not in func.botogram.pass_args:
        func.botogram.pass_args[id(func)] = []

    func.botogram.pass_args[id(func)].append("bot")
    return func


def pass_shared(func):
    """An handy decorator which passes the func's component's shared memory as
    first argument.

    Please note that the shared memory is passed only if the function is called
    by the bot itself, for example in an hook."""
    if not hasattr(func, "botogram"):
        func.botogram = utils.HookDetails(func)

    if id(func) not in func.botogram.pass_args:
        func.botogram.pass_args[id(func)] = []

    func.botogram.pass_args[id(func)].append("shared")
    return func


def help_message_for(func):
    """The return of the decorated function will be the help message of the
    function provided as an argument."""
    def decorator(help_func):
        if not hasattr(func, "botogram"):
            func.botogram = utils.HookDetails(func)

        func.botogram.help_message = help_func
        return help_func
    return decorator
