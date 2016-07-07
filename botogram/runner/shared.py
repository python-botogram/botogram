"""
    botogram.runner.shared
    Shared state driver for the botogram runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import collections
import functools

from . import ipc
from ..shared import drivers


class BotogramRunnerSharedLock(drivers.SharedObject):

    def _prepare(self):
        self.acquired = False
        self.queue = collections.deque()

    def restore(self, value):
        # Restore lock to a clean state
        self._prepare()

    def export(self):
        return self.acquired


class SharedStateBackend:

    def __init__(self):
        # The backend for the botogram runner driver simply forwards most of
        # the requests to an instance of a LocalDriver; this removes most of
        # the code duplication between the two drivers
        self._driver = drivers.LocalDriver()

        # Use a custom representation for shared locks
        self._driver._types_mapping["lock"] = BotogramRunnerSharedLock

    def __getattr__(self, name):
        # Don't forward private methods
        if name.startswith("_") or name in self.__dict__:
            return object.__getattribute__(self, name)

        return lambda args, reply: reply(getattr(self._driver, name)(*args))

    def _ensure_object(type):
        """Ensure the object exists and it's of that type"""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(self, args, reply):
                object_id = args[0]

                if object_id not in self._driver._objects:
                    raise ValueError("Object doesn't exist: %s" % object_id)

                obj = self._driver._objects[object_id]
                if obj.type != type:
                    raise TypeError("Operation not supported on the %s type" %
                                    obj.type)

                return f(self, reply, obj)
            return wrapper
        return decorator

    ############################
    #   Locks implementation   #
    ############################

    # Locks are implemented from scratch because we can't actually lock the IPC
    # process...

    @_ensure_object("lock")
    def lock_acquire(self, reply, obj):
        # If the object wasn't acquired just acquire it
        if not obj.acquired:
            print("Lock not acquired, releasing...")
            obj.acquired = True
            reply(True)
        else:
            print("Lock acquired, queueing...")
            # Schedule the reply for later
            # This blocks the caller, creating a lock-like situation
            obj.queue.appendleft(reply)

    @_ensure_object("lock")
    def lock_release(self, reply, obj):
        # If the object wasn
        if obj.acquired:
            # If there were some other processes in the queue for this lock
            # unlock the first of them, else just release the lock
            if obj.queue:
                new_owner_reply = obj.queue.pop()
                new_owner_reply(True)
            else:
                obj.acquired = False

        reply(True)
        return

    @_ensure_object("lock")
    def lock_status(self, reply, obj):
        reply(obj.acquired)


class BotogramRunnerDriver:

    def __init__(self, ipc_port, ipc_auth_key):
        self._ipc_port = ipc_port
        self._ipc_auth_key = ipc_auth_key

        # This is lazily loaded so the driver can be used even when the IPC
        # server isn't up yet
        self._ipc_cache = None

    def __reduce__(self):
        return rebuild_driver, (self._ipc_port, self._ipc_auth_key)

    @property
    def _ipc(self):
        if self._ipc_cache is None:
            self._ipc_cache = ipc.IPCClient(self._ipc_port, self._ipc_auth_key)
        return self._ipc_cache

    # Objects

    def object_list(self):
        return self._ipc.command("shared.object_list", tuple())

    def object_exists(self, id):
        return self._ipc.command("shared.object_exists", (id,))

    def object_type(self, id):
        return self._ipc.command("shared.object_type", (id,))

    def object_create(self, type, id):
        return self._ipc.command("shared.object_create", (type, id))

    # Dicts

    def dict_length(self, id):
        return self._ipc.command("shared.dict_length", (id,))

    def dict_item_get(self, id, key):
        return self._ipc.command("shared.dict_item_get", (id, key))

    def dict_item_set(self, id, key, value):
        return self._ipc.command("shared.dict_item_set", (id, key, value))

    def dict_item_delete(self, id, key):
        return self._ipc.command("shared.dict_item_delete", (id, key))

    def dict_contains(self, id, key):
        return self._ipc.command("shared.dict_contains", (id, key))

    def dict_keys(self, id):
        return self._ipc.command("shared.dict_keys", (id,))

    def dict_values(self, id):
        return self._ipc.command("shared.dict_values", (id,))

    def dict_items(self, id):
        return self._ipc.command("shared.dict_items", (id,))

    def dict_clear(self, id):
        return self._ipc.command("shared.dict_clenr", (id,))

    def dict_pop(self, id, key=drivers._None):
        return self._ipc.command("shared.dict_pop", (id, key))

    # Locks

    def lock_acquire(self, id):
        return self._ipc.command("shared.lock_acquire", (id,))

    def lock_release(self, id):
        return self._ipc.command("shared.lock_release", (id,))

    def lock_status(self, id):
        return self._ipc.command("shared.lock_status", (id,))

    # Importing and exporting

    def data_import(self, data):
        return self._ipc.command("shared.data_import", (data,))

    def data_export(self):
        return self._ipc.command("shared.data_export", tuple())
