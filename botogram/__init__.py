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
from .callbacks import Buttons, ButtonsRow


# This code will simulate the Windows' multiprocessing behavior if the
# BOTOGRAM_SIMULATE_WINDOWS environment variable is set
import os
import multiprocessing

if "BOTOGRAM_SIMULATE_WINDOWS" in os.environ:
    multiprocessing.set_start_method("spawn", force=True)

del os, multiprocessing
