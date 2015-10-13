"""
    botogram.shared
    Generic implementation of the shared memory

    Copyright (C) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


class LocalDriver:
    """Local driver for the shared memory"""

    def __init__(self):
        self._memories = {}

    def __reduce__(self):
        return rebuild_local_driver, (self.export_data(),)

    def get(self, component):
        # Create the shared memory if it doesn't exist
        new = False
        if component not in self._memories:
            self._memories[component] = {}
            new = True

        return self._memories[component], new

    def import_data(self, data):
        self._memories = data

    def export_data(self):
        return self._memories.copy()


class SharedMemory:
    """Implementation of the shared memory for one bot"""

    def __init__(self, driver=None):
        # The default driver is LocalDriver
        if driver is None:
            driver = LocalDriver()
        self.driver = driver

        self._inits = {}

    def __reduce__(self):
        return rebuild, (self.driver,)

    def _key_of(self, bot, component):
        """Get the key for a specific bot:component combination"""
        return bot+":"+component

    def register_inits_list(self, component, inits):
        """Register a new list to pick initializers from"""
        # Ignore the request if a list was already registered
        if component in self._inits:
            return

        self._inits[component] = inits

    def of(self, bot, component):
        """Get the shared memory of a specific component"""
        memory, is_new = self.driver.get(self._key_of(bot, component))

        # Be sure to initialize the shared memory if it's needed
        if is_new:
            self.apply_inits(component, memory)

        return memory

    def apply_inits(self, component, memory):
        """Apply all the inits of a component to a memory"""
        if component not in self._inits:
            return

        for init in self._inits[component]:
            init(memory)

    def switch_driver(self, driver=None):
        """Use another driver for this shared memory"""
        if driver is None:
            driver = LocalDriver()

        driver.import_data(self.driver.export_data())
        self.driver = driver


def rebuild(driver):
    return SharedMemory(driver)


def rebuild_local_driver(memories):
    obj = LocalDriver()
    obj.import_data(memories)

    return obj
