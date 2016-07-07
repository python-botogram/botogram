"""
    botogram.shared
    Generic implementation of the shared state

    Copyright (C) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import uuid
import fnmatch

from . import drivers
from . import proxies


class SharedBucket:
    """Implementation of a single, shared bucket"""

    def __init__(self, id, manager, driver):
        self._id = id
        self._manager = manager
        self._driver = driver

        # A cache for the objects this bucket contains
        self._objects = {}

        # Storage for object labels
        if not self.object_exists("__labels__"):
            self.create_object("dict", "__labels__")
        self._labels = self.get_object("__labels__")

        # Main instance of the shared memory of this bucket
        self.memory = self.object("dict", "__memory__")

    def object(self, type, label=None):
        """Get or create an object"""
        # If no ID was provided just create another object
        if label is None:
            return self.create_object(type)

        if label in self._labels:
            id = self._labels[label]
        else:
            id = str(uuid.uuid4())

            # Be sure to save the label
            if label is not None:
                self._labels[label] = id

        if self.object_exists(id):
            return self.get_object(id)
        return self.create_object(type, id)

    def lock(self, name):
        """Get a lock"""
        return self.object("lock", name)

    def create_object(self, type, id=None):
        """Create a new object in this bucket"""
        # If no ID is provided generate a new unique one
        if id is None:
            id = str(uuid.uuid4())

        id = "%s:%s" % (self._id, id)
        self._driver.object_create(type, id)

        proxy = self._manager._proxy_for(type)
        return proxy(id, self, self._driver)

    def get_object(self, id):
        """Get an existing object by its ID"""
        if not self.object_exists(id):
            raise NameError("Object with ID %s doesn't exist" % id)

        id = "%s:%s" % (self._id, id)
        proxy = self._manager._proxy_for(self._driver.object_type(id))
        return proxy(id, self, self._driver)

    def object_exists(self, id):
        """Check if an object exists"""
        id = "%s:%s" % (self._id, id)
        return self._driver.object_exists(id)


class SharedStateManager:
    """Manager of the shared state"""

    def __init__(self, driver=None):
        # The default driver is LocalDriver
        if driver is None:
            driver = drivers.LocalDriver()
        self._actual_driver = driver
        self._driver = proxies.DriverProxy(self._actual_driver)

        # Those are just stored locally on this instance
        self._memory_preparers = {}

        # Prepare the default proxies
        self._object_types = {}
        self.register_object_type("dict", proxies.DictProxy)
        self.register_object_type("lock", proxies.LockProxy)

        self._buckets = {}
        self._main_bucket = SharedBucket("__main__", self, self._driver)
        self._bucket_names = self._main_bucket.object("dict", "__buckets__")

    def bucket(self, name):
        """Create a new bucket"""
        is_new = False
        if name not in self._bucket_names:
            self._bucket_names[name] = str(uuid.uuid4())
            is_new = True

        id = self._bucket_names[name]
        if id not in self._buckets:
            self._buckets[id] = SharedBucket(id, self, self._driver)

        # Apply memory preparers only if the bucket is new
        if is_new:
            self.apply_memory_preparers(name, self._buckets[id])

        return self._buckets[id]

    def delete_bucket(self, name):
        """Delete an existing bucket"""
        if name not in self._bucket_names:
            raise NameError("Bucket %s doesn't exist")

        bucket_id = self._bucket_names.pop(name)

        # Delete all the objects part of that bucket
        bucket_id_prefix = "%s:" % bucket_id
        for obj_id in self._driver.objects_list():
            if obj_id.startswith(bucket_id_prefix):
                self._driver.objects_delete(obj_id)

        if bucket_id in self._buckets:
            del self._buckets[bucket_id]

    def add_memory_preparer(self, bucket, preparer):
        """Add a new memory preparer"""
        if bucket not in self._memory_preparers:
            self._memory_preparers[bucket] = []
        self._memory_preparers[bucket].append(preparer)

    def apply_memory_preparers(self, name, bucket):
        """Apply all the memory preparers to a bucket"""
        for pattern, preparers in self._memory_preparers.items():
            if not fnmatch.fnmatch(name, pattern):
                continue
            for preparer in preparers:
                preparer(bucket)

    def switch_driver(self, driver):
        """Switch to a new driver"""
        # Move the data from one driver to another
        data = self._actual_driver.data_export()
        driver.data_import(data)

        # Actually switch driver
        self._actual_driver = driver
        self._driver._switch_driver(driver)

    def register_object_type(self, name, proxy):
        """Register a new object type"""
        if name in self._object_types:
            raise NameError("A type with name %s already exists" % name)

        self._object_types[name] = proxy

    def _proxy_for(self, type):
        """Get the proxy for that specific type"""
        if type not in self._object_types:
            raise TypeError("Type %s doesn't exist" % type)

        return self._object_types[type]
