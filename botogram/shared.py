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

import threading
import functools
import builtins


class dict(builtins.dict):
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


class Lock:
    """Lock backed by the botogram's shared memory"""

    def __init__(self, parent, lock_id):
        self._parent = parent
        self._lock_id = lock_id

    @property
    def acquired(self):
        return self._parent.driver.lock_status(self._lock_id)

    def acquire(self):
        """Acquire the lock"""
        self._parent.driver.lock_acquire(self._lock_id)

    def release(self):
        """Release the lock"""
        self._parent.driver.lock_release(self._lock_id)

    __enter__ = acquire

    def __exit__(self, *__):
        self.release()


class SharedMemory:
    """Implementation of the shared memory for one bot"""

    def __init__(self, driver=None):
        # The default driver is LocalDriver
        if driver is None:
            driver = LocalDriver()
        self.driver = driver

        self._preparers = {}

    def __reduce__(self):
        return rebuild, (self.driver,)

    def _key_of(self, *parts):
        """Get the key for a shared item"""
        return ":".join(parts)

    def register_preparers_list(self, component, inits):
        """Register a new list to pick preparers from"""
        # Ignore the request if a list was already registered
        if component in self._preparers:
            return

        self._preparers[component] = inits

    def of(self, bot, component, *other):
        """Get the shared memory of a specific component"""
        memory, is_new = self.driver.get(self._key_of(bot, component, *other))

        # Treat as a standard shared memory only if no other names are provided
        if not other:
            # Be sure to initialize the shared memory if it's needed
            if is_new:
                self.apply_preparers(component, memory)

            # Add the lock method to the object
            memory.lock = functools.partial(self.lock, bot, component)

        return memory

    def apply_preparers(self, component, memory):
        """Apply all the preparers of a component to a memory"""
        if component not in self._preparers:
            return

        for preparer in self._preparers[component]:
            preparer.call(memory)

    def switch_driver(self, driver=None):
        """Use another driver for this shared memory"""
        if driver is None:
            driver = LocalDriver()

        driver.import_data(self.driver.export_data())
        self.driver = driver

    def lock(self, bot, component, name):
        """Get a shared lock"""
        return Lock(self, self._key_of(bot, component, name))


def rebuild(driver):
    return SharedMemory(driver)


def rebuild_local_driver(memories):
    obj = LocalDriver()
    obj.import_data(memories)

    return obj
