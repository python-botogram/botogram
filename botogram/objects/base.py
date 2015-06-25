"""
    botogram.objects.base
    Base classes and utilities for upstream API objects

    Copyright (c) 2015 Pietro Albini
    Released under the MIT license
"""


# This is used to make a reference to the current class while defining the
# fields table, since it's impossible to reference the class while defining it
_itself = object()


class BaseObject:
    """A base class for all of the API types"""

    _provide_api = True

    required = {}
    optional = {}

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

                # It's important to note that the value is validated passing
                # it in the field_type. This allows also automatic resolution
                # of types nesting
                if key in data:
                    # API instance is passed to the child if it wants it
                    if hasattr(field_type, "_provide_api"):
                        value = field_type(data[key], api)
                    else:
                        value = field_type(data[key])

                    setattr(self, key, value)

    def serialize(self):
        """Serialize this object"""
        result = {}

        for group, required in ((self.required, True), (self.optional, False)):
            for key, field_type in group.items():
                # A required key must be present
                if not hasattr(self, key) and required:
                    raise ValueError("The key %s must be present" % key)

                # Optional keys not present will be ignored
                if not hasattr(self, key):
                    continue

                result[key] = self._serialize_one(getattr(self, key))

        return result

    def _serialize_one(self, item):
        """Serialize one item"""
        if isinstance(item, BaseObject):
            return item.serialize()
        if isinstance(item, list):
            result = []
            for one in item:
                result.append(self._serialize_one(item))
            return result
        return item


def multiple(field_type):
    """_Accept a list of objects"""
    def __(objects, api):
        if not isinstance(objects, list):
            raise ValueError("multiple(%r) needs a list of objects"
                             % field_type)

        if hasattr(field_type, "_provide_api"):
            return [field_type(item, api) for item in objects]
        else:
            return [field_type(item) for item in objects]
    __._provide_api = True
    return __


def one_of(*field_types):
    """Accept one of these field types"""
    def __(object, api):
        # Try to use all of the types
        for field_type in field_types:
            try:
                if hasattr(field_type, "_provide_api"):
                    return field_type(object, api)
                else:
                    return field_type(object)
            except ValueError:
                pass
        raise ValueError("The object is neither a %s" % ", ".format(objects))
    __._provide_api = True
    return __
