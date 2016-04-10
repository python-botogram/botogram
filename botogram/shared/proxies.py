"""
    botogram.shared.proxies
    Object proxies for the botogram's shared memory

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import copy


# This is used as the default argument for some methods of DictProxy
_None = object()


class DictProxy:
    """A proxy for dictionaries"""

    def __init__(self, object_id, driver):
        self._object_id = object_id
        self._driver = driver

    def __str__(self):
        return str(dict(self.items()))

    def __repr__(self):
        return '<DictProxy with %s>' % self

    def __len__(self):
        return self._driver.dict_length(self._object_id)

    def __getitem__(self, key):
        return self._driver.dict_item_get(self._object_id, key)

    def __setitem__(self, key, value):
        self._driver.dict_item_set(self._object_id, key, value)

    def __delitem__(self, key):
        self._driver.dict_item_delete(self._object_id, key)

    def __contains__(self, key):
        return self._driver.dict_contains(self._object_id, key)

    def __iter__(self):
        return iter(self._driver.dict_keys(self._object_id))

    def clear(self):
        """Remove all items from the dictionary."""
        self._driver.dict_clear(self._object_id)

    def copy(self):
        """Return a shallow copy of the dictionary."""
        return dict(self._driver.dict_items(self._object_id))

    def get(self, key, default=_None):
        """Return the value for key if key is in the dictionary, else default.
        If default is not given, it defaults to None, so that this method never
        raises a KeyError.
        """
        try:
            return self._driver.dict_item_get(self._object_id, key)
        except KeyError:
            # Return a default value if provided
            if default is _None:
                raise
            return default

    def keys(self):
        """Return the dictionary's keys."""
        return self._driver.dict_keys(self._object_id)

    def values(self):
        """Return the dictionary's values."""
        return self._driver.dict_values(self._object_id)

    def items(self):
        """Return the dictionary's items."""
        return self._driver.dict_items(self._object_id)

    def pop(self, key, default=_None):
        """If key is in the dictionary, remove it and return its value, else
        return default. If default is not given and key is not in the
        dictionary, a KeyError is raised.
        """
        try:
            return self._driver.dict_pop(self._object_id, key)
        except KeyError:
            # Return a default value if provided
            if default is _None:
                raise
            return default

    def popitem(self):
        """Remove and return an arbitrary (key, value) pair from the
        dictionary.

        popitem() is useful to destructively iterate over a dictionary, as
        often used in set algorithms. If the dictionary is empty, calling
        popitem() raises a KeyError.
        """
        return self._driver.dict_pop(self._object_id)

    def setdefault(self, key, default=None):
        """If key is in the dictionary, return its value. If not, insert key
        with a value of default and return default. default defaults to None.
        """
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other=_None, **kwargs)
        """Update the dictionary with the key/value pairs from other,
        overwriting existing keys. Return None.

        update() accepts either another dictionary object or an iterable of
        key/value pairs (as tuples or other iterables of length two). If
        keyword arguments are specified, the dictionary is then updated with
        those key/value pairs: d.update(red=1, blue=2).
        """
        # Support providing data as a keyword argument
        if other is _None:
            other = kwargs

        # Accept also non-dict objects
        if type(other) == dict:
            other = dict.items()

        # Add every value to our dictionary
        for key, value in other:
            self[key] = value
