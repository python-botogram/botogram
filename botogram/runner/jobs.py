"""
    botogram.runner.jobs
    Definition of the jobs runner workers' can execute

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


class Job:
    """A job processed by workers"""

    def __init__(self, bot_id, func, metadata):
        self.bot_id = bot_id
        self.func = func
        self.metadata = metadata

    def process(self, bots):
        bot = bots[self.bot_id]
        return self.func(bot, self.metadata)


def process_update(bot, metadata):
    """Process an update received from Telegram"""
    update = metadata["update"]

    # Restore the removed API object
    update.set_api(bot.api)
    bot.process(update)
