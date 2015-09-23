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
        if component not in self._memories:
            self._memories[component] = {}

        return self._memories[component]

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

    def __reduce__(self):
        return rebuild, (self.driver,)

    def of(self, bot, component):
        """Get the shared memory of a specific component"""
        return self.driver.get(bot+":"+component)

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
