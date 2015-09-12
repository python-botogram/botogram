"""
    botogram.shared
    Generic implementation of the shared memory

    Copyright (C) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


class SharedMemory:
    """Implementation of the shared memory for one bot"""

    def __init__(self):
        self._memories = {}

    def __reduce__(self):
        return rebuild, (self._memories,)

    def of(self, component):
        """Get the shared memory of a specific component"""
        if component not in self._memories:
            self._init_memory(component)

        return self._memories[component]

    def _init_memory(self, component):
        self._memories[component] = dict()


def rebuild(memories):
    obj = SharedMemory()
    obj._memories = memories

    return obj
