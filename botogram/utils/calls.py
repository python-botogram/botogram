"""
    botogram.utils.calls
    Utilities for dynamic function args

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import inspect

import functools


def wraps(func):
    """Update a wrapper function to looks like the wrapped one"""
    # A custom implementation of functools.wraps is needed because we need some
    # more metadata on the returned function
    def updater(original):
        # Here the original signature is needed in order to call the function
        # with the right set of arguments in Bot._call
        original_signature = inspect.signature(original)

        updated = functools.update_wrapper(original, func)
        updated._botogram_original_signature = original_signature
        return updated
    return updater


class CallLazyArgument:
    """A special argument which is loaded lazily"""

    _botogram_call_lazy_argument = True

    def __init__(self, loader):
        self.loader = loader

    def load(self):
        return self.loader()


def call(func, **available):
    """Call a function with a dynamic set of arguments"""
    # Get the correct function signature
    # _botogram_original_signature contains the signature used before wrapping
    # a function with @utils.wraps, so the arguments gets resolved correctly
    if hasattr(func, "_botogram_original_signature"):
        signature = func._botogram_original_signature
    else:
        signature = inspect.signature(func)

    kwargs = {}
    for name in signature.parameters:
        if name not in available:
            raise TypeError("botogram doesn't know what to provide for %s"
                            % name)

        # If the argument is lazily loaded wake him up
        arg = available[name]
        if hasattr(arg, "_botogram_call_lazy_argument"):
            arg = arg.load()

        kwargs[name] = arg

    return func(**kwargs)
