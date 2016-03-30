"""
    botogram.utils
    Utilities used by the rest of the code

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import re
import os
import sys
import gettext
import traceback
import inspect

import pkg_resources
import logbook
import functools

# URLs regex created by http://twitter.com/imme_emosol

_username_re = re.compile(r"\@([a-zA-Z0-9_]{5}[a-zA-Z0-9_]*)")
_command_re = re.compile(r"^\/[a-zA-Z0-9_]+(\@[a-zA-Z0-9_]{5}[a-zA-Z0-9_]*)?$")
_email_re = re.compile(r"[a-zA-Z0-9_\.\+\-]+\@[a-zA-Z0-9_\.\-]+\.[a-zA-Z]+")
_url_re = re.compile(r"https?://(-\.)?([^\s/?\.#]+\.?)+(/[^\s]*)?")

# This small piece of global state will track if logbook was configured
_logger_configured = False


warn_logger = logbook.Logger("botogram's code warnings")


def _deprecated_message(name, removed_on, fix, back):
    before = "%s will be removed in botogram %s." % (name, removed_on)
    after = "Fix: %s" % fix
    warn(back - 1, before, after)


def deprecated(name, removed_on, fix):
    """Mark a function as deprecated"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            _deprecated_message(name, removed_on, fix, -2)
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


def wraps(func):
    """Update a wrapper function to looks like the wrapped one"""
    # A custom implementation of functools.wraps is needed because we need some
    # more metadata on the returned function
    def updater(original):
        # Here the original signature is needed in order to call the function
        # with the right set of arguments in Bot._call
        original_signature = inspect.signature(original)

        updated = functools.update_wrapper(original, func)
        updated.botogram_original_signature = original_signature
        return updated
    return updater


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


def docstring_of(func, bot=None, component_id=None, format=False):
    """Get the docstring of a function"""
    # Get the correct function from the hook
    if hasattr(func, "_botogram_hook"):
        func = func.func

    if hasattr(func, "_botogram_help_message"):
        if bot is not None:
            docstring = bot._call(func._botogram_help_message, component_id)
        else:
            docstring = func._botogram_help_message()
    elif func.__doc__:
        docstring = func.__doc__
    # Put a default message
    else:
        if bot is not None:
            docstring = bot._("No description available.")
        else:
            docstring = "No description available."

        if format:
            docstring = "<i>%s</i>" % docstring

    return format_docstr(docstring)


def strip_urls(string):
    """Strip URLs and emails from a string"""
    string = _url_re.sub("", string)
    string = _email_re.sub("", string)
    return string


def usernames_in(message):
    """Return all the matched usernames in the message"""
    # Don't parse usernames in the commands
    if _command_re.match(message.split(" ", 1)[0]):
        message = message.split(" ", 1)[1]

    # Strip email addresses from the message, in order to avoid matching the
    # user's domain. Also strip URLs, in order to avoid usernames in them.
    message = strip_urls(message)

    results = []
    for result in _username_re.finditer(message):
        if result.group(1):
            results.append(result.group(1))

    return results


def get_language(lang):
    """Get the GNUTranslations instance of a specific language"""
    path = pkg_resources.resource_filename("botogram", "i18n/%s.mo" % lang)
    if not os.path.exists(path):
        raise ValueError('Language "%s" is not supported by botogram' % lang)

    with open(path, "rb") as f:
        gt = gettext.GNUTranslations(f)

    return gt


def configure_logger():
    """Configure a logger object"""
    global _logger_configured

    # Don't configure the logger multiple times
    if _logger_configured:
        return

    # The StreamHandler will log everything to stdout
    min_level = 'DEBUG' if 'BOTOGRAM_DEBUG' in os.environ else 'INFO'
    handler = logbook.StreamHandler(sys.stdout, level=min_level)
    handler.format_string = '{record.time.hour:0>2}:{record.time.minute:0>2}' \
                            '.{record.time.second:0>2} - ' \
                            '{record.level_name:^9} - {record.message}'
    handler.push_application()

    # Don't reconfigure the logger, thanks
    _logger_configured = True
