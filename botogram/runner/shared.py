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

import collections
import multiprocessing
import multiprocessing.managers


class OverrideableDict(dict):
    pass


class SharedMemoryCommands:
    """Definition of IPC commands for the shared memory"""

    def __init__(self):
        self._memories = {}
        self._manager = multiprocessing.managers.SyncManager()

        self._locks = set()
        self._locks_queues = {}

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

    def lock_acquire(self, lock_id, reply):
        """Acquire a lock"""
        # If the lock isn't acquired acquire it
        if lock_id not in self._locks:
            self._locks.add(lock_id)
            return reply(None)

        # Else ignore the request, and add the reply function to the queue
        if lock_id not in self._locks_queues:
            self._locks_queues[lock_id] = collections.deque()
        self._locks_queues[lock_id].appendleft(reply)

    def lock_release(self, lock_id, reply):
        """Release a lock"""
        # If the lock wasn't acquired, just return
        if lock_id not in self._locks:
            return reply(None)

        self._locks.remove(lock_id)

        # If there are processes waiting for this lock, wake up one of them
        if lock_id in self._locks_queues:
            self._locks_queues[lock_id].pop()(None)
            # And clear up the queue if it's empty
            if not len(self._locks_queues[lock_id]):
                del self._locks_queues[lock_id]

        reply(None)

    def lock_status(self, lock_id, reply):
        """Check if a lock was acquired"""
        reply(lock_id in self._locks)

    def lock_import(self, locks, reply):
        """Bulk import all the locks"""
        self._locks = set(locks)
        self._locks_queues = {}
        reply(None)

    def lock_export(self, __, reply):
        """Export all the locks"""
        reply(self._locks)


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

    def lock_acquire(self, lock_id):
        # This automagically blocks if the lock is already acquired
        self._command("shared.lock_acquire", lock_id)

    def lock_release(self, lock_id):
        self._command("shared.lock_release", lock_id)

    def lock_status(self, lock_id):
        return self._command("shared.lock_status", lock_id)

    def import_data(self, data):
        # This will merge the provided component with the shared memory
        for memory_id, memory in data["storage"].items():
            memory = self.get(memory_id)
            memory.update(data)

        if len(data["locks"]):
            self._command("shared.lock_import", data["locks"])

    def export_data(self):
        result = {"storage": {}}
        for memory_id, data in self._memories.items():
            result["storage"][memory_id] = dict(data)

        result["locks"] = self._command("shared.lock_export", None)

        return result


def rebuild_driver():
    return MultiprocessingDriver()
