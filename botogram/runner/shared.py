"""
    botogram.runner.shared
    Shared state driver for the botogram runner

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from . import ipc
from ..shared import drivers


class SharedStateBackend:

    def __init__(self):
        # The backend for the botogram runner driver simply forwards the
        # requests to an instance of a LocalDriver; this removes most of the
        # code duplication between the two drivers
        self._driver = drivers.LocalDriver()

    def __getattr__(self, name):
        # Don't forward private methods
        if name.startswith("_") or name in self.__dict__:
            return object.__getattribute__(self, name)

        return lambda args, reply: reply(getattr(self._driver, name)(*args))

    # TODO: implement custom supports for locks since they currently don't work


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
