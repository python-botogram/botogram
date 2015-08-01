"""
    botogram.runner.processes
    Definition of all of the running processes

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import sys
import os
import traceback
import queue

from .. import objects


class BaseProcess(multiprocessing.Process):
    """Base class for all of the processes"""

    def __init__(self, runner, updates, bot, *args):
        self.runner = runner
        self.stop = False
        self.updates_queue = updates
        self.bot = bot
        self.logger = bot.logger

        super(BaseProcess, self).__init__()
        self.setup(*args)

    def setup(self, *args):
        """Setup the class"""
        pass

    def run(self):
        """Run the process"""
        self.logger.debug("%s process is ready! (pid: %s)", self.name,
                          os.getpid())
        while not self.stop:
            try:
                self.loop()
            except (KeyboardInterrupt, InterruptedError):
                self.on_stop()
            except:
                traceback.print_exc()

        self.logger.debug("%s process with pid %s just stopped", self.name,
                          os.getpid())

    def loop(self):
        """One single loop"""
        pass

    def on_stop(self):
        """When the process is stopping"""
        self.stop = True


class WorkerProcess(BaseProcess):
    """This process will execute all the updates it receives"""

    name = "Worker"

    def setup(self):
        self.will_stop = False

    def loop(self):
        try:
            update = self.updates_queue.get(True, 0.2)
        except queue.Empty:
            # If the worker should be stopped and no updates are in the queue,
            # then gracefully stop
            if self.will_stop:
                self.stop = True
            return

        # If the update is None, stop the worker
        if update is None:
            self.stop = True
            return

        self.bot.process(update)

    def on_stop(self):
        self.will_stop = True


class UpdaterProcess(BaseProcess):
    """This process will fetch the updates"""

    name = "Updater"

    def setup(self, commands_queue):
        self.last_id = -1
        self.commands_queue = commands_queue
        self.backlog_processed = False

        # This will process the backlog if the programmer wants so
        if self.bot.process_backlog:
            self.backlog_processed = True

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
        }, expect=objects.Updates)

        for update in updates:
            self.last_id = update.update_id

            if not self.backlog_processed:
                if update.message.date < self.runner._started_at:
                    self.logger.debug("Update #%s skipped because it's coming "
                                      "from the backlog." % update.update_id)
                    continue
                self.backlog_processed = True

            self.logger.debug("Successifully queued update #%s!" %
                              update.update_id)
            self.updates_queue.put(update)
