"""
    botogram.runner.shared
    Shared memory implementation for the botogram runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import multiprocessing
import multiprocessing.managers


class SharedMemoryCommands:
    """Definition of IPC commands for the shared memory"""

    def __init__(self):
        self._memories = {}
        self._manager = multiprocessing.managers.SyncManager()

    def start(self):
        """Start the shared memory manager"""
        self._manager.start()

    def get(self, memory_id, reply):
        """Get the shared memory which has the provided ID"""
        new = False
        if memory_id not in self._memories:
            self._memories[memory_id] = self._manager.dict()
            new = True

        # Send the shared memory to the process which requested it
        reply((self._memories[memory_id], new))

    def list(self, memory_id, reply):
        """Get all the shared memories available"""
        reply(list(self._memories.keys()))


class MultiprocessingDriver:
    """This is a multiprocessing-ready driver for the shared memory"""

    def __init__(self):
        self._memories = {}

    def __reduce__(self):
        return rebuild_driver, tuple()

    def _command(self, command, arg):
        """Send a command"""
        ipc = multiprocessing.current_process().ipc
        return ipc.command(command, arg)

    def get(self, memory_id):
        # Create the shared memory if it doens't exist
        is_new = False
        if memory_id not in self._memories:
            memory, is_new = self._command("shared.get", memory_id)
            self._memories[memory_id] = memory

        return self._memories[memory_id], is_new

    def import_data(self, data):
        # This will merge the provided component with the shared memory
        for memory_id, memory in data.items():
            memory = self.get(memory_id)
            memory.update(data)

    def export_data(self):
        result = {}
        for memory_id, data in self._memories.items():
            result[memory_id] = dict(data)

        return result


def rebuild_driver():
    return MultiprocessingDriver()
