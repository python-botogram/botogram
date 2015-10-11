"""
    botogram.runner.jobs
    Definition of the jobs runner workers' can execute

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import collections


class JobsCommands:
    """This object will manage the IPC jobs.* commands"""

    def __init__(self):
        self.queue = collections.deque()
        self.waiting = collections.deque()

        self.stop = False

    def put(self, job, reply):
        """Put a job in the queue"""
        if self.stop:
            reply("No more jobs accepted", ok=False)
            return

        # Directly send the job to the processes wanting it
        if len(self.waiting) > 0:
            try:
                self.waiting.pop()(job)
            except EOFError:
                pass
            else:
                reply(None)
                return

        self.queue.appendleft(job)
        reply(None)

    def get(self, _, reply):
        """Get a job from the queue"""
        # If there is something in the queue return it, else append the request
        # to the new jobs' waiting deque
        if len(self.queue) > 0:
            reply(self.queue.pop())
        else:
            if self.stop:
                reply("__stop__")

            self.waiting.appendleft(reply)

    def shutdown(self, _, reply):
        """Shutdown the queue"""
        self.stop = True

        # Stop all the waiting workers
        if len(self.waiting) > 0:
            for worker in self.waiting:
                worker("__stop__")

        reply(None)


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
