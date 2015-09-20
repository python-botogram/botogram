"""
    botogram
    A Python microframework for Telegram bots

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""
# flake8: noqa

from .bot import Bot, create
from .frozenbot import FrozenBotError
from .components import Component
from .decorators import pass_bot, pass_shared, help_message_for
from .objects import *
from .utils import usernames_in


# This code will simulate the Windows' multiprocessing behavior if the
# BOTOGRAM_SIMULATE_WINDOWS environment variable is set
import os
import multiprocessing

if "BOTOGRAM_SIMULATE_WINDOWS" in os.environ:
    multiprocessing.set_start_method("spawn", force=True)

del os, multiprocessing
