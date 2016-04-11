"""
    botogram.shared
    Generic implementation of the shared memory

    Copyright (C) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import functools

from . import drivers
from . import proxies


class SharedMemory:
    """Implementation of the shared memory for one bot"""

    def __init__(self, driver=None):
        # The default driver is LocalDriver
        if driver is None:
            driver = drivers.LocalDriver()
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
            driver = drivers.LocalDriver()

        driver.import_data(self.driver.export_data())
        self.driver = driver

    def lock(self, bot, component, name):
        """Get a shared lock"""
        return Lock(self, self._key_of(bot, component, name))


def rebuild(driver):
    return SharedMemory(driver)
