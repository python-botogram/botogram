"""
    botogram.runner.shared
    Shared memory implementation for the botogram runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import queue
import multiprocessing
import multiprocessing.managers


class SharedMemoryManager:
    """Manage shared memory in the botogram runner"""

    def __init__(self):
        self._memories = {}
        self._queues = []
        self._manager = multiprocessing.managers.SyncManager()

    def get(self, memory_id):
        """Get the shared memory of a given bot:component"""
        if memory_id not in self._memories:
            self._memories[memory_id] = self._manager.dict()
        return self._memories[memory_id]

    def get_driver(self, bot_id):
        """Get a new driver for the shared memory"""
        return MultiprocessingDriver(bot_id, *self._get_commands_queue())

    def _get_commands_queue(self):
        """Get a new queue for commands"""
        commands = multiprocessing.Queue()
        responses = multiprocessing.Queue()
        self._queues.append((commands, responses))
        return commands, responses

    def process_commands(self):
        """Process commands from the drivers"""
        for commands, responses in self._queues:
            # Get a new command from the queue
            try:
                message = commands.get(False)
            except queue.Empty:
                continue

            # memory <memoryid>
            if message.startswith("memory"):
                memory = self.get(message.split(" ", 1)[1])
                responses.put(memory)

            # new_queue
            elif message.startswith("new_queue"):
                new_q = self._get_commands_queue()
                responses.put(new_q)

    def start(self):
        """Start the background process"""
        self._manager.start()

    def stop(self):
        """Stop the background process"""
        self._manager.shutdown()


class MultiprocessingDriver:
    """This is a multiprocessing-ready driver for the shared memory"""

    def __init__(self, bot_id, commands, responses):
        self._bot_id = bot_id
        self._commands = commands
        self._responses = responses
        self._memories = {}

    def __reduce__(self):
        new_commands, new_responses = self._command("new_queue")
        return rebuild_driver, (self._bot_id, new_commands, new_responses)

    def _command(self, *args):
        """Send a command to the manager"""
        self._commands.put(" ".join(args))
        return self._responses.get()

    def get(self, component):
        # Create the shared memory if it doens't exist
        if component not in self._memories:
            memory = self._command("memory", self._bot_id+":"+component)
            self._memories[component] = memory

        return self._memories[component]

    def import_data(self, data):
        # This will merge the provided component with the shared memory
        for component, memory in data.items():
            memory = self.get(component)
            memory.update(data)

    def export_data(self):
        result = {}
        for component, data in self._memories.items():
            result[component] = dict(data)

        return result


def rebuild_driver(bot_id, commands, responses):
    return MultiprocessingDriver(bot_id, commands, responses)
