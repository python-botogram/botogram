"""
    botogram.runner
    A multi-process, scalable bot runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import time
import atexit
import signal

from . import processes


class BotogramRunner:
    """A multi-process, scalable bot runner"""

    def __init__(self, bot, workers=2):
        self.bot = bot
        self.processes = []
        self.running = False
        self._stop = False
        self._started_at = None

        self._workers_count = workers

        self._setup_shared()
        self._setup_signals()

    def _setup_shared(self):
        """Setup processes-shared things"""
        self._updates_queue = multiprocessing.Queue()
        self._updater_commands = multiprocessing.Queue()

    def _setup_signals(self):
        """Setup signals handlers"""
        atexit.register(self.stop)

        # Register stop to all the signals
        for one in signal.SIGINT, signal.SIGTERM:
            signal.signal(one, self.stop)

    def run(self):
        """Run the runner"""
        if self.running:
            raise RuntimeError("Server already running")
        self.running = True
        self._started_at = time.time()

        self._define_processes()

        for process in self.processes:
            process.start()

        # Main server loop
        while not self._stop:
            time.sleep(0.2)

        for process in self.processes:
            process.join()
            self.processes.remove(process)

        self.running = False
        self._stop_signal = False
        self._started_at = None

    def stop(self, *__):
        """Stop a running runner"""
        # This will stop all the workers
        for i in range(self._workers_count):
            self._updates_queue.put(None)

        self._updater_commands.put(None)
        self._stop = True

    def _define_processes(self):
        """Define all the processes"""
        updater = processes.UpdaterProcess(self, self._updates_queue, self.bot,
                                           self._updater_commands)
        self.processes.append(updater)

        for i in range(self._workers_count):
            self.processes.append(processes.WorkerProcess(self,
                                                          self._updates_queue,
                                                          self.bot))
