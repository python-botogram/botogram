"""
    botogram
    A Python microframework for Telegram bots

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


# Prepare the logger
from .utils import configure_logger
configure_logger()
del configure_logger


# flake8: noqa

from .api import APIError, ChatUnavailableError
from .bot import Bot, create, channel
from .frozenbot import FrozenBotError
from .components import Component
from .decorators import pass_bot, pass_shared, help_message_for
from .runner import run
from .objects import *
from .utils import usernames_in


# This code will simulate the Windows' multiprocessing behavior if the
# BOTOGRAM_SIMULATE_WINDOWS environment variable is set
import os
import multiprocessing

if "BOTOGRAM_SIMULATE_WINDOWS" in os.environ:
    multiprocessing.set_start_method("spawn", force=True)

del os, multiprocessing
