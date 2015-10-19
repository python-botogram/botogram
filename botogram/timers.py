"""
    botogram.timers
    Core implementation of timers

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import time


class TimerJob:
    """Representation of a single job"""

    def __init__(self, interval, bot_id, func):
        self.interval = interval
        self.bot_id = bot_id
        self.func = func
        self.last_run = -interval

    def now(self, current=None):
        """Check if the timer should be ran now"""
        # Allow to provide a dummy time
        if current is None:
            current = time.time()

        res = self.last_run+self.interval <= current

        # Increment the last_run if the result is True
        if res:
            self.last_run = current

        return res

    def process(self, bots):
        """Process the job"""
        bot = bots[self.bot_id]
        return bot._call(self.func)


class Scheduler:
    """Schedule all the timers"""

    def __init__(self):
        self.jobs = []

    def add(self, job):
        """Add a job to the scheduler"""
        self.jobs.append(job)

    def now(self, current=None):
        """Return which jobs should be scheduled now"""
        # Allow to provide a dummy time
        if current is None:
            current = time.time()

        # Return all the jobs which should be executed now
        for job in self.jobs:
            if not job.now(current):
                continue
            yield job
