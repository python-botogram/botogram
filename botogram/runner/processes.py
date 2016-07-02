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
from . import shared
from . import ipc
from .. import objects
from .. import api


class BaseProcess(multiprocessing.Process):
    """Base class for all of the processes"""

    def __init__(self, ipc_info, *args):
        self.stop = False
        self.logger = logbook.Logger("botogram subprocess")

        self.ipc = None
        if ipc_info is not None:
            self.ipc = ipc.IPCClient(*ipc_info)

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
            except ipc.IPCServerCrashedError:
                self.logger.error("The IPC server just crashed. Please kill "
                                  "the runner.")
                self.on_stop()
            except (KeyboardInterrupt, InterruptedError):
                self.on_stop()
            except:
                traceback.print_exc()

        self.after_stop()

        # Be sure to close the IPC connection
        if self.ipc:
            self.ipc.close()

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


class IPCProcess(BaseProcess):
    """This process will handle IPC requests"""

    name = "IPC"

    def setup(self, ipc):
        self.ipc_server = ipc

        # Setup the jobs commands
        self.jobs_commands = jobs.JobsCommands()
        ipc.register_command("jobs.put", self.jobs_commands.put)
        ipc.register_command("jobs.bulk_put", self.jobs_commands.bulk_put)
        ipc.register_command("jobs.get", self.jobs_commands.get)
        ipc.register_command("jobs.shutdown", self.jobs_commands.shutdown)

        # Setup the shared commands
        self.shared_commands = shared.SharedMemoryCommands()
        ipc.register_command("shared.get", self.shared_commands.get)
        ipc.register_command("shared.list", self.shared_commands.list)
        ipc.register_command("shared.lock_acquire",
                             self.shared_commands.lock_acquire)
        ipc.register_command("shared.lock_release",
                             self.shared_commands.lock_release)
        ipc.register_command("shared.lock_status",
                             self.shared_commands.lock_status)
        ipc.register_command("shared.lock_import",
                             self.shared_commands.lock_import)
        ipc.register_command("shared.lock_export",
                             self.shared_commands.lock_export)

    def before_start(self):
        # Start the shared memory manager
        self.shared_commands.start()

    def loop(self):
        self.ipc_server.run()

        # This will stop running the loop
        super(IPCProcess, self).on_stop()

    def on_stop(self):
        super(IPCProcess, self).on_stop()

        self.ipc_server.stop = True


class WorkerProcess(BaseProcess):
    """This process will execute all the updates it receives"""

    name = "Worker"

    def setup(self, bots):
        self.bots = bots

    def loop(self):
        # Request a new job
        try:
            job = self.ipc.command("jobs.get", None)
        except InterruptedError:
            # This return acts as a continue
            return

        # If the job is None, stop the worker
        if job == "__stop__":
            self.stop = True
            return

        # Run the wanted job
        job.process(self.bots)


class UpdaterProcess(BaseProcess):
    """This process will fetch the updates"""

    name = "Updater"

    def setup(self, bot, commands):
        self.bot = bot
        self.bot_id = bot._bot_id
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
                "offset": self.last_id + 1,
                "timeout": 1,
            }, expect=objects.Updates)
        except (api.APIError, ValueError, TypeError) as e:
            self.logger.error("An error occured while fetching updates!")
            self.logger.debug("Exception type: %s" % e.__class__.__name__)
            self.logger.debug("Exception content: %s" % str(e))
            return

        for update in updates:
            # botogram 0.2.x doesn't support anything but messages, ignore the
            # other things -- Fix issue GH-70
            if update.message is None:
                continue

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
            self.ipc.command("jobs.put", job)


def _ignore_signal(*__):
    pass
