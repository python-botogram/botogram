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
