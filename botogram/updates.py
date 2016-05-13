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


class AnotherInstanceRunningError(FetchError):
    """Another instance of your bot is running somewhere else"""

    def __init__(self):
        Exception.__init__(self, "Request terminated because of another long "
                           "pooling or webhook active")


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

    def _fetch_updates(self, timeout):
        """Low level function to just fetch updates from Telegram"""
        try:
            return self._bot.api.call("getUpdates", {
                "offset": self._last_id + 1,
                "timeout": timeout,
            }, expect=objects.Updates)
        except api.APIError as e:
            # Raise a specific exception if another instance is running
            if e.error_code == 409 and "conflict" in e.description.lower():
                raise AnotherInstanceRunningError()
            raise
        except ValueError:
            raise FetchError("Got an invalid response from Telegram!")

    def fetch(self, timeout=1):
        """Fetch the latest updates"""
        updates = self._fetch_updates(timeout)

        # If there are no updates just ignore this block
        try:
            self._last_id = updates[-1].update_id
        except IndexError:
            pass

        if self._backlog_processed:
            return updates, []

        # Now start to filter backlog from messages to process
        # This is faster than a plain check for every item with a for, and
        # helps a lot if you have a *really* long backlog

        if not updates:
            self._backlog_processed = True
            return [], []

        to_check = len(updates) - 1
        check_chunk = len(updates)
        direction = -1  # -1 is backward, 1 is forward
        last = 0

        while True:
            # Check if the current message to check is from the backlog
            # Adjust the check direction accordingly
            update = updates[to_check]
            if update.message.date < self._started_at:
                direction = 1
            else:
                direction = -1

            # The next chunk to check is exactly half of the previous one
            check_chunk = int(check_chunk / 2)
            if check_chunk == 0:
                check_chunk = 1

            # If the last one was from the backlog, the current one is not and
            # this is at the max precision (step of 1), then consider it as
            # found
            if direction == 1 and last == -1 and check_chunk == 1:
                to_check += 1  # Return to the previous state
                self._backlog_processed = True
                break
            last = direction

            # Set the next update to check
            to_check += direction * check_chunk

            # If the next update to check is outside the bounds of the list
            # just break the loop (and say the backlog is processed if no
            # updates are from it)
            if to_check < 0:
                self._backlog_processed = True
                break
            elif to_check >= len(updates):
                break

        # The first is the updates to process, the second the backlog
        return updates[to_check:], updates[:to_check]

    def block_until_alone(self, treshold=4, check_timeout=1, when_stop=None):
        """Returns when this one is the only instance of the bot"""
        checks_count = 0

        while checks_count < treshold:
            # This provides an artificial end to the blocking
            if when_stop is not None and when_stop():
                return False

            try:
                updates = self._fetch_updates(check_timeout)
            except AnotherInstanceRunningError:
                # Reset the count
                checks_count = 0
                continue

            # Update the last_id
            try:
                self._last_id = updates[-1].update_id
            except IndexError:
                pass

            # Don't count requests with new updates, since they don't tell if
            # another instance is running, they only make noise
            if updates:
                continue

            # Increment the count every time a request succedes, so the whole
            # function exits when checks_needed is reached
            checks_count += 1

        return True

    @property
    def backlog_processed(self):
        return self._backlog_processed
