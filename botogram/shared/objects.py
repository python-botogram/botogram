"""
    botogram.shared.objects
    Underlying objects for the shared memory

    Copyright (C) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


_None = object()


class SharedObject:
    """A shared object"""

    def __init__(self, id, type, value=_None, standalone=False):
        self.id = id
        self.type = type
        self.standalone = standalone

        self.children = set()
        self.parents = set()

        if type == "dict":
            self.content = dict()
        elif type == "lock":
            self.content = False
        else:
            raise TypeError("Unsupported type: %s" % type)

    def add_child(self, object):
        """Add a child object"""
        # Add a dual link between objects
        self.children.add(object)
        object.parents.add(self)

    def remove_child(self, object):
        """Remove a child object"""
        if object in self.children:
            # Remove the dual link
            self.children.remove(object)
            object.parents.remove(self)
