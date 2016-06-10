"""
    botogram.updates
    Updates fetching and initial processing

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

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
        if not self._backlog_processed:
            # Just erase all the previous messages
            last = self._bot.api.call("getUpdates", {
                "offset": -1,
                "timeout": 0,
            }, expect=objects.Updates)

            # Be sure to skip also the last update
            if last:
                self._last_id = last[-1].update_id
            else:
                self._last_id = 0

            self._backlog_processed = True

        updates = self._fetch_updates(timeout)

        # If there are no updates just ignore this block
        try:
            self._last_id = updates[-1].update_id
        except IndexError:
            pass

        return updates

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
