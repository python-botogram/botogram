"""
    botogram.runner
    A multi-process, scalable bot runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import multiprocessing.managers
import time
import atexit
import signal
import logbook

from . import processes
from . import shared


class BotogramRunner:
    """A multi-process, scalable bot runner"""

    def __init__(self, *bots, workers=2):
        # Only frozen instances, thanks
        self._bots = {bot._bot_id: bot.freeze() for bot in bots}

        self._updater_processes = {}
        self._worker_processes = []

        self.running = False
        self._stop = False
        self._started_at = None

        # Create a new memory manager and apply a new driver to all the bots
        self._shared_memory = shared.SharedMemoryManager()
        for bot_id, bot in self._bots.items():
            driver = self._shared_memory.get_driver()
            bot._shared_memory.switch_driver(driver)

        self._workers_count = workers

        self.logger = logbook.Logger("botogram runner")

    def run(self):
        """Run the runner"""
        if self.running:
            raise RuntimeError("Server already running")

        self.logger.info("The botogram runner is booting up.")
        self.logger.info("Press Ctrl+C to exit.")

        self.running = True
        self._started_at = time.time()

        self._enable_signals()
        self._shared_memory.start()
        to_workers, to_updaters = self._boot_processes()

        try:
            # Main server loop
            while not self._stop:
                self._shared_memory.process_commands()
                time.sleep(0.1)
        except (KeyboardInterrupt, InterruptedError):
            pass

        self._shutdown_processes(to_workers, to_updaters)
        self._shared_memory.stop()

        self.running = False
        self._started_at = None

    def stop(self, *__):
        """Stop a running runner"""
        self._stop = True

    def _boot_processes(self):
        """Start all the used processes"""
        queue = multiprocessing.Queue()
        upd_commands = multiprocessing.Queue()

        # Boot up all the worker processes
        for i in range(self._workers_count):
            worker = processes.WorkerProcess(self, queue)
            worker.start()

            self._worker_processes.append(worker)

        # Boot up all the updater processes
        for id, bot in self._bots.items():
            updater = processes.UpdaterProcess(self, id, queue, upd_commands)
            updater.start()

            self._updater_processes[id] = updater

        return queue, upd_commands

    def _shutdown_processes(self, to_workers, to_updaters):
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
        for i in range(len(self._worker_processes)):
            to_workers.put(None)
        for worker in self._worker_processes:
            worker.join()
        self._worker_processes = []

    def _enable_signals(self):
        """Setup signals handlers"""
        atexit.register(self.stop)

        # Register stop to all the signals
        for one in signal.SIGINT, signal.SIGTERM:
            signal.signal(one, self.stop)
