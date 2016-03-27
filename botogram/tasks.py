"""
    botogram.tasks
    Core implementation of tasks and timers

    Copyright (c) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import time


class BaseTask:
    """A basic task"""

    def __init__(self, hook):
        self.hook = hook

    def process(self, bot):
        """Process the task"""
        if hasattr(self.hook, "call"):
            return self.hook.call(bot)
        return self.hook(bot)


class TimerTask(BaseTask):
    """Representation of a single timer"""

    def __init__(self, interval, hook):
        self.interval = interval
        self.last_run = -interval

        super(TimerTask, self).__init__(hook)

    def now(self, current=None):
        """Check if the timer should be ran now"""
        # Allow to provide a dummy time
        if current is None:
            current = time.time()

        res = self.last_run + self.interval <= current

        # Increment the last_run if the result is True
        if res:
            self.last_run = current

        return res


class Scheduler:
    """Schedule all the tasks"""

    def __init__(self):
        # Each component will add its own list here
        self.tasks_lists = []

        self.tasks = []
        self.tasks_lists.append(self.tasks)

    def add(self, task):
        """Add a task to the scheduler"""
        self.tasks.append(task)

    def register_tasks_list(self, tasks):
        """Register a new list of tasks"""
        self.tasks_lists.append(tasks)

    def now(self, current=None):
        """Return which tasks should be scheduled now"""
        # Allow to provide a dummy time
        if current is None:
            current = time.time()

        # Return all the tasks which should be executed now
        for tasks in self.tasks_lists:
            for task in tasks:
                if not task.now(current):
                    continue
                yield task
