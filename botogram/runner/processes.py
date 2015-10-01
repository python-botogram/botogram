"""
    botogram.runner.processes
    Definition of all of the running processes

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import os
import traceback
import queue
import time
import signal

import logbook

from . import jobs
from .. import objects
from .. import api


class BaseProcess(multiprocessing.Process):
    """Base class for all of the processes"""

    def __init__(self, *args):
        self.stop = False
        self.logger = logbook.Logger("botogram subprocess")

        super(BaseProcess, self).__init__()
        self.setup(*args)

    def setup(self, *args):
        """Setup the class"""
        pass

    def run(self):
        """Run the process"""
        for one in signal.SIGINT, signal.SIGTERM:
            signal.signal(one, _ignore_signal)

        self.before_start()

        self.logger.debug("%s process is ready! (pid: %s)" % (self.name,
                          os.getpid()))
        while not self.stop:
            try:
                self.loop()
            except (KeyboardInterrupt, InterruptedError):
                self.on_stop()
            except:
                traceback.print_exc()

        self.after_stop()

        self.logger.debug("%s process with pid %s just stopped" % (self.name,
                          os.getpid()))

    def loop(self):
        """One single loop"""
        pass

    def before_start(self):
        """Before the process starts"""
        pass

    def after_stop(self):
        """After the process stops"""
        pass

    def on_stop(self):
        """When the process is stopping"""
        self.stop = True


class SharedMemoryProcess(BaseProcess):
    """This process will manage commands for shared memory's drivers"""

    name = "Shared"

    def setup(self, manager):
        self.manager = manager

    def loop(self):
        result = self.manager.process_commands()

        # result == False means the process should stop
        if result is False:
            self.stop = True

    def before_start(self):
        self.manager.initialize()
        self.manager.start()

    def after_stop(self):
        self.manager.stop()


class WorkerProcess(BaseProcess):
    """This process will execute all the updates it receives"""

    name = "Worker"

    def setup(self, bots, queue):
        self.bots = bots
        self.queue = queue
        self.will_stop = False

    def loop(self):
        try:
            job = self.queue.get(True, 0.1)
        except queue.Empty:
            # If the worker should be stopped and no jobs in the queue,
            # then gracefully stop
            if self.will_stop:
                self.stop = True
            return

        # If the job is None, stop the worker
        if job is None:
            self.stop = True
            return

        # Run the wanted job
        job.process(self.bots)

    def on_stop(self):
        self.will_stop = True


class UpdaterProcess(BaseProcess):
    """This process will fetch the updates"""

    name = "Updater"

    def setup(self, bot, to_workers, commands):
        self.bot = bot
        self.bot_id = bot._bot_id
        self.to_workers = to_workers
        self.commands = commands

        self.started_at = time.time()

        self.backlog_processed = False
        self.last_id = -1

        # This will process the backlog if the programmer wants so
        if self.bot.process_backlog:
            self.backlog_processed = True

    def loop(self):
        # This allows to control the process
        try:
            command = self.commands.get(False)

            # The None command will stop the process
            if command == "stop":
                self.stop = True
                return
        except queue.Empty:
            pass

        try:
            updates = self.bot.api.call("getUpdates", {
                "offset": self.last_id+1,
                "timeout": 1,
            }, expect=objects.Updates)
        except (api.APIError, ValueError, TypeError) as e:
            self.logger.error("An error occured while fetching updates!")
            self.logger.debug("Exception type: %s" % e.__class__.__name__)
            self.logger.debug("Exception content: %s" % str(e))
            return

        for update in updates:
            self.last_id = update.update_id

            if not self.backlog_processed:
                if update.message.date < self.started_at:
                    self.logger.debug("Update #%s skipped because it's coming "
                                      "from the backlog." % update.update_id)
                    continue
                self.backlog_processed = True

            self.logger.debug("Successifully queued update #%s!" %
                              update.update_id)

            # No dynamic data is left to the update
            # The API will be re-added after
            update.set_api(None)
            job = jobs.Job(self.bot_id, jobs.process_update, {
                "update": update,
            })
            self.to_workers.put(job)


def _ignore_signal(*__):
    pass
