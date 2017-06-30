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
