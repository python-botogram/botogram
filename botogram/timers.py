"""
    botogram.timers
    Core implementation of timers

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import time


class TimerJob:
    """Representation of a single job"""

    def __init__(self, interval, func):
        self.interval = interval
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

    def process(self, bot):
        """Process the job"""
        return bot._call(self.func)


class Scheduler:
    """Schedule all the timers"""

    def __init__(self):
        # Each component will add its own list here
        self.jobs_lists = []

        self.jobs = []
        self.jobs_lists.append(self.jobs)

    def add(self, job):
        """Add a job to the scheduler"""
        self.jobs.append(job)

    def register_jobs_list(self, jobs):
        """Register a new list of jobs"""
        self.jobs_lists.append(jobs)

    def now(self, current=None):
        """Return which jobs should be scheduled now"""
        # Allow to provide a dummy time
        if current is None:
            current = time.time()

        # Return all the jobs which should be executed now
        for jobs in self.jobs_lists:
            for job in jobs:
                if not job.now(current):
                    continue
                yield job
