"""
    botogram.utils.warns
    Utilities about warns and deprecations

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import sys
import traceback

import logbook


warn_logger = logbook.Logger("botogram's code warnings")


def _deprecated_message(name, removed_on, fix, back):
    before = "%s will be removed in botogram %s." % (name, removed_on)
    after = "Fix: %s" % fix
    warn(back - 1, before, after)


def deprecated(name, removed_on, fix, back=0):
    """Mark a function as deprecated"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            _deprecated_message(name, removed_on, fix, -2 - back)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class DeprecatedAttributes:
    """Mark a class attribute as deprecated"""

    _deprecated_ = {}

    def __getattribute__(self, key):
        def get(k):
            return object.__getattribute__(self, k)

        deprecated = get("_deprecated_")

        if key in deprecated:
            _deprecated_message(
                get("__class__").__name__ + "." + key,
                deprecated[key]["removed_on"],
                deprecated[key]["fix"],
                -2,
            )
            if "callback" in deprecated[key]:
                return deprecated[key]["callback"]()

        return object.__getattribute__(self, key)


def warn(stack_pos, before_message, after_message=None):
    """Issue a warning caused by user code"""
    # This is a workaround for http://bugs.python.org/issue25108
    # In Python 3.5.0, traceback.extract_stack returns an additional internal
    # stack frame, which causes a lot of trouble around there.
    if sys.version_info[:3] == (3, 5, 0):
        stack_pos -= 1

    frame = traceback.extract_stack()[stack_pos - 1]
    at_message = "At: %s (line %s)" % (frame[0], frame[1])

    warn_logger.warn(before_message)
    if after_message is not None:
        warn_logger.warn(at_message)
        warn_logger.warn(after_message + "\n")
    else:
        warn_logger.warn(at_message + "\n")
