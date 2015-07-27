"""
    botogram.objects.base
    Base classes and utilities for upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


# This is used to make a reference to the current class while defining the
# fields table, since it's impossible to reference the class while defining it
_itself = object()


class BaseObject:
    """A base class for all of the API types"""

    required = {}
    optional = {}
    replace_keys = {}

    def __init__(self, data, api=None):
        self._api = api

        # Populate the namespace
        for group, required in ((self.required, True), (self.optional, False)):
            for key, field_type in group.items():
                # A required key must be present
                if key not in data and required:
                    raise ValueError("The key %s must be present" % key)

                # If the field type is _itself, replace it with this class
                if field_type is _itself:
                    field_type = self.__class__

                # Replace the keys -- useful for reserved keywords
                new_key = key
                if key in self.replace_keys:
                    new_key = self.replace_keys[key]

                # Don't resolve non-present keys
                if key not in data:
                    setattr(self, new_key, None)
                    continue

                # It's important to note that the value is validated passing
                # it in the field_type. This allows also automatic resolution
                # of types nesting
                setattr(self, new_key, field_type(data[key]))

    def set_api(self, api):
        """Change the API instance"""
        self._api = api

        # Recursively set the API
        for key in list(self.required.keys())+list(self.optional.keys()):
            if not hasattr(self, key):
                continue
            value = getattr(self, key)

            # Update the API, if it supports that
            if hasattr(value, "set_api"):
                value.set_api(api)

    def serialize(self):
        """Serialize this object"""
        result = {}

        for group, required in ((self.required, True), (self.optional, False)):
            for key, field_type in group.items():
                # Replace the keys -- useful for reserved keywords
                new_key = key
                if key in self.replace_keys:
                    new_key = self.replace_keys[key]

                # A required key must be present
                if not hasattr(self, new_key) and required:
                    raise ValueError("The key %s must be present" % new_key)

                # Optional keys not present will be ignored
                if not hasattr(self, new_key):
                    continue

                # Empty keys will be ignored
                if getattr(self, new_key) is None:
                    continue

                result[key] = self._serialize_one(getattr(self, new_key))

        return result

    def _serialize_one(self, item):
        """Serialize one item"""
        if isinstance(item, BaseObject):
            return item.serialize()
        if isinstance(item, list):
            result = []
            for one in item:
                result.append(self._serialize_one(one))
            return result
        return item


class _MultipleList(list):
    """Custom list which adds the set_api method"""

    def set_api(self, api):
        """Set the API on a multiple() result"""
        for item in self:
            if hasattr(item, "set_api"):
                item.set_api(api)


def multiple(field_type):
    """_Accept a list of objects"""
    def __(objects):
        if not isinstance(objects, list):
            raise ValueError("multiple(%r) needs a list of objects"
                             % field_type)

        return _MultipleList([field_type(item) for item in objects])
    return __


def one_of(*field_types):
    """Accept one of these field types"""
    def __(object):
        # Try to use all of the types
        for field_type in field_types:
            try:
                return field_type(object)
            except ValueError:
                pass
        raise ValueError("The object is neither a %s" % ", ".format(objects))
    return __
