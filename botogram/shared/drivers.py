"""
    botogram.shared.drivers
    Builtin generic drivers for the shared memory

    Copyright (C) 2015-2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import builtins
import threading
import uuid
import functools


# This is used as the default argument for some methods of DictProxy
_None = object()


class dict(builtins.dict):
    # This class is overridden like this because this is the only way to add
    # dynamic attributes at runtime
    pass


class SharedObject:

    def __init__(self, type):
        self.id = id
        self.type = type
        self.children = set()
        self.parents = set()

        if type == "dict":
            self.value = dict()

    def add_child(self, id):
        """Register a new child"""
        self.children.add(id)

    def remove_child(self, id):
        """Remove a child"""
        try:
            self.children.remove(id)
        except KeyError:
            pass


class LocalDriver:
    """Local driver for the shared memory"""

    def __init__(self):
        self._objects = {}

    def __reduce__(self):
        return rebuild_local_driver, (self.export_data(),)

    def create_object(self, type, id=None, parent=None):
        """Create a new object"""
        if id is None:
            id = uuid.uuid4()

        self._objects[id] = SharedObject(id, type)
        if parent is not None:
            self._objects[parent].add_child(id)
            self._objects[id].add_parent(parent)
        else:
            self._objects[id].add_parent(None)

        return self._objects[id]

    def delete_object(self, id):
        """Delete an object"""
        obj = self._objects.pop(id)

        # Recursively delete every children
        for child in obj.children:
            self.delete_object(child)

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

                return f(self, obj.value, *args, **kwargs)
            return wrapper
        return decorator

    ############################
    #   dicts implementation   #
    ############################

    @_ensure_object("dict")
    def dict_length(self, obj):
        return len(obj)

    @_ensure_object("dict")
    def dict_item_get(self, obj, key):
        return obj[key]

    @_ensure_object("dict")
    def dict_item_set(self, obj, key, value):
        obj[key] = value

    @_ensure_object("dict")
    def dict_item_delete(self, obj, key):
        del obj[key]

    @_ensure_object("dict")
    def dict_contains(self, obj, key):
        return key in obj

    @_ensure_object("dict")
    def dict_keys(self, obj):
        return tuple(obj.keys())

    @_ensure_object("dict")
    def dict_values(self, obj):
        return tuple(obj.values())

    @_ensure_object("dict")
    def dict_items(self, obj):
        return tuple(obj.items())

    @_ensure_object("dict")
    def dict_clear(self, obj):
        obj.clear()

    @_ensure_object("dict")
    def dict_pop(self, obj, key=_None):
        # If no keys are provided pop a random item
        if key is _None:
            return obj.popitem()
        else:
            return obj.pop(key)

    ############################
    #   Locks implementation   #
    ############################

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
