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
        pass


class SharedDict(SharedObject):

    def _prepare(self):
        self.value = {}


class SharedLock(SharedObject):

    def _prepare(self):
        self.lock = threading.Lock()
        self.acquired = False


class LocalDriver:
    """Local driver for the shared memory"""

    def __init__(self):
        self._objects = {}

    def __reduce__(self):
        return rebuild_local_driver, (self.export_data(),)

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
    #   objects implemnetation   #
    ##############################

    def object_list(self):
        """List all the objects this driver contains"""
        return list(self._objects.keys())

    def object_exists(self, id):
        """Check if a specific object exists"""
        return id in self._objects

    def object_type(self, id):
        """Get the type of an object"""
        return self._objects[id].type

    def object_create(self, type, id):
        """Create a new object"""
        if id in self._objects:
            raise NameError("An object with id %s already exists!" % id)

        if type == "dict":
            cls = SharedDict
        elif type == "lock":
            cls = SharedLock
        else:
            raise TypeError("Unsupported type: %s" % type)

        self._objects[id] = cls(id, type)
        return self._objects[id]

    def object_delete(self, id):
        """Delete an object"""
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

    def import_data(self, data):
        # Rebuild the objects
        self._objects = {}
        for id, value in data["objects"]:
            if type(value) == dict:
                self._objects[id] = SharedObject("dict")
                self._objects[id].value = value
            else:
                raise ValueError("Unsupported type: %s" % type(value))

        # Rebuild the locks
        self._locks = {}
        for lock_id in data["locks"]:
            self.lock_acquire(lock_id)

    def export_data(self):
        # Get an exportable format for both objects and locks
        objects = {id: {
            "value": obj.value,
            "children": obj.children,
        } for id, obj in self._objects.items()}

        locks = [lock_id for lock_id, d in self._locks if not d["acquired"]]

        return {"storage": objects, "locks": locks}


def rebuild_local_driver(memories):
    obj = LocalDriver()
    obj.import_data(memories)

    return obj
