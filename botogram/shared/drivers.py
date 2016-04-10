"""
    botogram.shared.drivers
    Builtin generic drivers for the shared memory

    Copyright (C) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import builtins
import threading


class dict(builtins.dict):
    # This class is overridden like this because this is the only way to add
    # dynamic attributes at runtime
    pass


class LocalDriver:
    """Local driver for the shared memory"""

    def __init__(self):
        self._memories = {}
        self._locks = {}

    def __reduce__(self):
        return rebuild_local_driver, (self.export_data(),)

    def get(self, component):
        # Create the shared memory if it doesn't exist
        new = False
        if component not in self._memories:
            self._memories[component] = dict()
            new = True

        return self._memories[component], new

    def lock_acquire(self, lock_id):
        # Create a new lock if it doesn't exist yet
        if lock_id not in self._locks:
            self._locks[lock_id] = {"obj": threading.Lock(), "acquired": False}

        self._locks[lock_id]["obj"].acquire()
        self._locks[lock_id]["acquired"] = True

    def lock_release(self, lock_id):
        if lock_id not in self._locks:
            return

        self._locks[lock_id]["acquired"] = False
        self._locks[lock_id].release()

    def lock_status(self, lock_id):
        if lock_id not in self._locks:
            return False

        return self._locks[lock_id]["acquired"]

    def import_data(self, data):
        self._memories = dict(data["storage"])

        # Rebuild the locks
        self._locks = {}
        for lock_id in data["locks"]:
            self.lock_acquire(lock_id)

    def export_data(self):
        locks = [lock_id for lock_id, d in self._locks if not d["acquired"]]
        return {"storage": self._memories.copy(), "locks": locks}


def rebuild_local_driver(memories):
    obj = LocalDriver()
    obj.import_data(memories)

    return obj
