# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

import multiprocessing
import os
import traceback
import queue
import signal

import logbook

from . import jobs
from . import shared
from . import ipc
from .. import api
from .. import updates as updates_module


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

        self.fetcher = updates_module.UpdatesFetcher(bot)

    def should_stop(self):
        """Check if the process should stop"""
        try:
            command = self.commands.get(False)
        except queue.Empty:
            val = False
        else:
            val = command == "stop"

        self.stop = val
        return val

    def loop(self):
        # This allows to control the process
        if self.should_stop():
            return

        try:
            updates = self.fetcher.fetch()
        except updates_module.AnotherInstanceRunningError:
            self.handle_another_instance()
            return
        except api.APIError as e:
            self.logger.error("An error occured while fetching updates!")
            self.logger.debug("Exception type: %s" % e.__class__.__name__)
            self.logger.debug("Exception content: %s" % str(e))
            return

        if not updates:
            return

        result = []
        for update in updates:
            update.set_api(None)
            result.append(jobs.Job(self.bot_id, jobs.process_update, {
                "update": update,
            }))

        self.ipc.command("jobs.bulk_put", result)

    def handle_another_instance(self):
        """Code run when another instance of the bot is running"""
        # Tell the user what's happening
        self.logger.error("Another instance of this bot is running!")
        self.logger.error("Please close any other instance of the bot, and "
                          "this one will start working again")
        self.logger.error("If you can't find other instances just revoke the "
                          "API token")

        # Wait until the other instances are closed
        result = self.fetcher.block_until_alone(when_stop=self.should_stop)

        if result:
            self.logger.info("This instance is now the only one. The bot is "
                             "working again")


def _ignore_signal(*__):
    pass
