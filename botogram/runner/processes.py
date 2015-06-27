"""
    botogram.runner.processes
    Definition of all of the running processes

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import sys
import traceback
import queue

from .. import objects


class BaseProcess(multiprocessing.Process):
    """Base class for all of the processes"""

    def __init__(self, updates, bot, *args):
        self.stop = False
        self.updates_queue = updates
        self.bot = bot

        super(BaseProcess, self).__init__()
        self.setup(*args)

    def setup(self, *args):
        """Setup the class"""
        pass

    def run(self):
        """Run the process"""
        while not self.stop:
            try:
                self.loop()
            except:
                traceback.print_exc()

    def loop(self):
        """One single loop"""
        pass


class WorkerProcess(BaseProcess):
    """This process will execute all the updates it receives"""

    def loop(self):
        update = self.updates_queue.get()

        # If the update is None, stop the worker
        if update is None:
            self.stop = True
            return

        self.bot.process(update)


class UpdaterProcess(BaseProcess):
    """This process will fetch the updates"""

    def setup(self, commands_queue):
        self.last_id = -1
        self.commands_queue = commands_queue

    def loop(self):
        try:
            command = self.commands_queue.get(False)

            # The None command will stop the process
            if command is None:
                self.stop = True
                return
        except queue.Empty:
            pass

        api = self.bot.api
        updates = api.call("getUpdates", {
            "offset": self.last_id+1,
            "timeout": 1,
        }, objects.Updates)

        for update in updates:
            self.updates_queue.put(update)
            self.last_id = update.update_id
