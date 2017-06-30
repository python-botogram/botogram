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
import multiprocessing.managers
import time
import atexit
import signal
import logbook

from . import processes
from . import shared
from . import ipc
from . import jobs


class BotogramRunner:
    """A multi-process, scalable bot runner"""

    def __init__(self, *bots, workers=2):
        # Only frozen instances, thanks
        self._bots = {bot._bot_id: bot.freeze() for bot in bots}

        self._updater_processes = {}
        self._worker_processes = []
        self._ipc_process = None
        self.ipc = None

        self.running = False
        self._stop = False
        self._started_at = None
        self._last_scheduled_checks = -1

        # Start the IPC server
        self._ipc_server = ipc.IPCServer()
        self.ipc_port = self._ipc_server.port
        self.ipc_auth_key = self._ipc_server.auth_key
        self._ipc_stop_key = self._ipc_server.stop_key

        # Use the MultiprocessingDriver for all the shared memories
        for bot in self._bots.values():
            bot._shared_memory.switch_driver(shared.MultiprocessingDriver())

        self._workers_count = workers

        self.logger = logbook.Logger("botogram runner")

    def run(self):
        """Run the runner"""
        if self.running:
            raise RuntimeError("Server already running")

        self.logger.debug("Booting up the botogram runner...")
        self.logger.debug("IPC address: 127.0.0.1:%s" % self.ipc_port)
        self.logger.debug("IPC auth key: %s" % self.ipc_auth_key)

        self.running = True
        self._started_at = time.time()

        self._enable_signals()
        to_updaters = self._boot_processes()

        self.logger.info("Your bot is now running!")
        self.logger.info("Press Ctrl+C to exit.")

        try:
            # Main server loop
            while not self._stop:
                self._loop()
                time.sleep(0.1)
        except (KeyboardInterrupt, InterruptedError):
            pass

        self._shutdown_processes(to_updaters)

        self.running = False
        self._started_at = None
        self._last_scheduled_checks = -1

    def _loop(self):
        """The main loop"""
        # Check for scheduled tasks
        now = int(time.time())
        if now > self._last_scheduled_checks:
            self._last_scheduled_checks = now

            jobs_list = []
            for bot in self._bots.values():
                for task in bot.scheduled_tasks(current_time=now, wrap=False):
                    jobs_list.append(jobs.Job(bot._bot_id, jobs.process_task, {
                        "task": task,
                    }))
            # Don't put jobs into the queue if there are no jobs
            if jobs_list:
                self.ipc.command("jobs.bulk_put", jobs_list)

    def stop(self, *__):
        """Stop a running runner"""
        self._stop = True

    def _boot_processes(self):
        """Start all the used processes"""
        upd_commands = multiprocessing.Queue()

        # Boot up the IPC process
        ipc_process = processes.IPCProcess(None, self._ipc_server)
        ipc_process.start()
        self._ipc_process = ipc_process

        # And boot the client
        # This will wait until the IPC server is started
        ipc_info = (self.ipc_port, self.ipc_auth_key)
        while True:
            try:
                self.ipc = ipc.IPCClient(*ipc_info)
                break
            except ConnectionRefusedError:
                time.sleep(0.1)

        # Boot up all the worker processes
        for i in range(self._workers_count):
            worker = processes.WorkerProcess(ipc_info, self._bots)
            worker.start()

            self._worker_processes.append(worker)

        # Boot up all the updater processes
        for bot in self._bots.values():
            updater = processes.UpdaterProcess(ipc_info, bot, upd_commands)
            updater.start()

            self._updater_processes[id] = updater

        return upd_commands

    def _shutdown_processes(self, to_updaters):
        """Shutdown all the opened processes"""
        self.logger.info("Shutting down the runner...")

        # Shutdown updaters before, and after the workers
        # This way no update will be lost
        for i in range(len(self._updater_processes)):
            to_updaters.put("stop")
        for process in self._updater_processes.values():
            process.join()
        self._updaters_processes = {}

        # Here, we tell each worker to shut down, and then we join it
        self.ipc.command("jobs.shutdown", None)
        for worker in self._worker_processes:
            worker.join()
        self._worker_processes = []

        # And finally we stop the IPC process
        self.ipc.command("__stop__", self._ipc_stop_key)
        self._ipc_process.join()
        self.ipc = None

    def _enable_signals(self):
        """Setup signals handlers"""
        atexit.register(self.stop)

        # Register stop to all the signals
        for one in signal.SIGINT, signal.SIGTERM:
            signal.signal(one, self.stop)


def run(*bots, **options):
    """Run multiple bots at once"""
    runner = BotogramRunner(*bots, **options)
    runner.run()
