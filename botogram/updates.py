"""
    botogram.updates
    Updates fetching and initial processing

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import time

from . import objects
from . import api


class FetchError(api.APIError):
    """Something went wrong while fetching updates"""
    pass


class UpdatesFetcher:
    """Logic for fetching updates"""

    def __init__(self, bot):
        self._bot = bot
        self._last_id = -1
        self._started_at = time.time()
        self._backlog_processed = False

        # Don't treat backlog as backlog if bot.process_backlog is True
        if bot.process_backlog:
            self._backlog_processed = True

    def fetch(self, timeout=1):
        """Fetch the latest updates"""
        try:
            updates = self._bot.api.call("getUpdates", {
                "offset": self._last_id + 1,
                "timeout": timeout,
            }, expect=objects.Updates)
        except ValueError as e:
            raise FetchError("Got an invalid response from Telegram!")

        # If there are no updates just ignore this block
        try:
            self._last_id = updates[-1].update_id
        except IndexError:
            pass

        if self._backlog_processed:
            return updates, []

        result = []
        backlog = []
        for update in updates:
            if update.message.date < self._started_at:
                backlog.append(update)
                continue

            result.append(update)
            self._backlog_processed = True

        return result, backlog

    @property
    def backlog_processed(self):
        return self._backlog_processed
