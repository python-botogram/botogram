"""
    botogram.shared.drivers
    Builtin generic drivers for the shared state

    Copyright (C) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import builtins
import threading
import uuid
import functools


# This is used as the default argument for some methods of DictProxy
_None = object()


class SharedObject:

    def __init__(self, id, type):
        self.id = id
        self.type = type

        self._prepare()

    def _prepare(self):
        raise NotImplementedError

    def export(self):
        raise NotImplementedError

    def restore(self):
        raise NotImplementedError


class SharedDict(SharedObject):

    def _prepare(self):
        self.value = {}

    def restore(self, value):
        self.value = value

    def export(self):
        return self.value.copy()


class SharedLock(SharedObject):

    def _prepare(self):
        self.lock = threading.Lock()
        self.acquired = False

    def restore(self, value):
        # Restore lock to a clean state
        self._prepare()

    def export(self):
        return self.acquired


class LocalDriver:
    """Local driver for the shared memory"""

    def __init__(self):
        self._objects = {}

        self._types_mapping = {
            "dict": SharedDict,
            "lock": SharedLock,
        }

    def __reduce__(self):
        return rebuild_local_driver, (self.data_export(),)

    def _ensure_object(type):
        """Ensure the object exists and it's of that type"""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(self, object_id, *args, **kwargs):
                if object_id not in self._objects:
                    raise ValueError("Object doesn't exist: %s" % object_id)

                obj = self._objects[object_id]
                if obj.type != type:
                    raise TypeError("Operation not supported on the %s type" %
                                    obj.type)

                return f(self, obj, *args, **kwargs)
            return wrapper
        return decorator

    ##############################
    #   objects implementation   #
    ##############################

    def object_list(self):
        return list(self._objects.keys())

    def object_exists(self, id):
        return id in self._objects

    def object_type(self, id):
        return self._objects[id].type

    def object_create(self, type, id):
        if id in self._objects:
            raise NameError("An object with id %s already exists!" % id)

        try:
            cls = self._types_mapping[type]
        except KeyError:
            raise TypeError("Unsupported type: %s" % type)

        self._objects[id] = cls(id, type)

    def object_delete(self, id):
        if id in self._objects:
            del self._objects[id]

    ############################
    #   dicts implementation   #
    ############################

    @_ensure_object("dict")
    def dict_length(self, obj):
        return len(obj.value)

    @_ensure_object("dict")
    def dict_item_get(self, obj, key):
        return obj.value[key]

    @_ensure_object("dict")
    def dict_item_set(self, obj, key, value):
        obj.value[key] = value

    @_ensure_object("dict")
    def dict_item_delete(self, obj, key):
        del obj.value[key]

    @_ensure_object("dict")
    def dict_contains(self, obj, key):
        return key in obj.value

    @_ensure_object("dict")
    def dict_keys(self, obj):
        return tuple(obj.value.keys())

    @_ensure_object("dict")
    def dict_values(self, obj):
        return tuple(obj.value.values())

    @_ensure_object("dict")
    def dict_items(self, obj):
        return tuple(obj.value.items())

    @_ensure_object("dict")
    def dict_clear(self, obj):
        obj.value.clear()

    @_ensure_object("dict")
    def dict_pop(self, obj, key=_None):
        # If no keys are provided pop a random item
        if key is _None:
            return obj.value.popitem()
        else:
            return obj.value.pop(key)

    ############################
    #   Locks implementation   #
    ############################

    @_ensure_object("lock")
    def lock_acquire(self, obj):
        obj.lock.acquire()
        obj.acquired = True

    @_ensure_object("lock")
    def lock_release(self, obj):
        obj.acquired = False
        obj.lock.release()

    @_ensure_object("lock")
    def lock_status(self, obj):
        return obj.acquired

    ###############################
    #   Importing and exporting   #
    ###############################

    def data_import(self, data):
        """Import data from another driver"""
        for id, content in data.items():
            self.object_create(content["type"], id)
            self._objects[id].restore(content["value"])

    def data_export(self):
        """Export the data contained in this driver"""
        result = {}
        for obj in self._objects.values():
            result[obj.id] = {"type": obj.type, "value": obj.export()}

        return result


def rebuild_local_driver(data):
    obj = LocalDriver()
    obj.data_import(data)

    return obj
