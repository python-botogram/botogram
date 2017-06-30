# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.


# This is used to make a reference to the current class while defining the
# fields table, since it's impossible to reference the class while defining it
_itself = object()


class BaseObject:
    """A base class for all of the API types"""

    required = {}
    optional = {}
    replace_keys = {}
    _check_equality_ = None

    def __init__(self, data, api=None):
        # Prevent receiving strange types
        if not isinstance(data, dict):
            raise ValueError("A dict must be provided")

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

        if api is not None:
            self.set_api(api)

    def __eq__(self, other):
        to_check = self._check_equality_

        if to_check is None:
            return id(self) == id(other)

        if not isinstance(other, self.__class__):
            return False

        return getattr(self, to_check) == getattr(other, to_check)

    def set_api(self, api):
        """Change the API instance"""
        self._api = api

        # Recursively set the API
        for key in list(self.required.keys()) + list(self.optional.keys()):
            # Be sure to use the right key
            if key in self.replace_keys:
                key = self.replace_keys[key]

            value = getattr(self, key)
            if value is None:
                continue

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
