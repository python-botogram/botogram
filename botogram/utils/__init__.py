"""
    botogram.utils
    Utilities used by the rest of the code

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

# flake8: noqa

from .deprecations import deprecated, DeprecatedAttributes, warn
from .strings import strip_urls, usernames_in
from .startup import get_language, configure_logger
from .calls import wraps, CallLazyArgument, call
