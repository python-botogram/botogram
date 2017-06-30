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

from .base import BaseObject
from . import mixins


class PhotoSize(BaseObject, mixins.FileMixin):
    """Telegram API representation of a photo size

    https://core.telegram.org/bots/api#photosize
    """

    required = {
        "file_id": str,
        "width": int,
        "height": int,
    }
    optional = {
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Photo(mixins.FileMixin):
    """Custom representation of a photo

    The current API provided by Telegram for photos sucks, so this tries to
    provide a better one.
    """

    def __init__(self, data, api=None):
        self._api = api
        # Accept only lists of PhotoSize
        if not isinstance(data, list):
            raise ValueError("You must provide a list of PhotoSize")

        # A photo without sizes is nothing
        if len(data) == 0:
            raise ValueError("No sizes passed...")

        # Put all the sizes in an array
        self.sizes = []
        for size in data:
            self.sizes.append(PhotoSize(size, api))

        # Calculate the smaller and the biggest sizes
        with_size = {}
        for size in self.sizes:
            with_size[size.height * size.width] = size
        self.smallest = with_size[min(with_size.keys())]
        self.biggest = with_size[max(with_size.keys())]

        # Publish all the attributes of the biggest-size photo
        attrs = list(PhotoSize.required.keys())
        attrs += list(PhotoSize.optional.keys())
        for attr in attrs:
            setattr(self, attr, getattr(self.biggest, attr))

    def __eq__(self, other):
        return isinstance(other, Photo) and self.sizes == other.sizes

    def set_api(self, api):
        """Change the API instance"""
        self._api = api

        # Set the API on all the photo sizes
        for size in self.sizes:
            size.set_api(api)

    def serialize(self):
        """Serialize this object"""
        result = []
        for size in self.sizes:
            result.append(size.serialize())

        return result


class Audio(BaseObject, mixins.FileMixin):
    """Telegram API representation of an audio track

    https://core.telegram.org/bots/api#audio
    """

    required = {
        "file_id": str,
        "duration": int,
    }
    optional = {
        "performer": str,
        "title": str,
        "mime_type": str,
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Voice(BaseObject, mixins.FileMixin):
    """Telegram API representation of a voice message

    https://core.telegram.org/bots/api#voice
    """

    required = {
        "file_id": str,
        "duration": int,
    }
    optional = {
        "mime_type": str,
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Document(BaseObject, mixins.FileMixin):
    """Telegram API representation of a document

    https://core.telegram.org/bots/api#document
    """

    required = {
        "file_id": str,
    }
    optional = {
        "thumb": PhotoSize,
        "file_name": str,
        "mime_type": str,
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Sticker(BaseObject, mixins.FileMixin):
    """Telegram API representation of a sticker

    https://core.telegram.org/bots/api#sticker
    """

    required = {
        "file_id": str,
        "width": int,
        "height": int,
    }
    optional = {
        "thumb": PhotoSize,
        "emoji": str,
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Video(BaseObject, mixins.FileMixin):
    """Telegram API representation of a video

    https://core.telegram.org/bots/api#video
    """

    required = {
        "file_id": str,
        "width": int,
        "height": int,
        "duration": int,
    }
    optional = {
        "thumb": PhotoSize,
        "mime_type": str,
        "file_size": int,
    }
    _check_equality_ = "file_id"


class Contact(BaseObject):
    """Telegram API representation of a contact

    https://core.telegram.org/bots/api#contact
    """

    required = {
        "phone_number": str,
        "first_name": str,
    }
    optional = {
        "last_name": str,
        "user_id": int,
    }
    _check_equality_ = "phone_number"


class Location(BaseObject):
    """Telegram API representation of a location mark

    https://core.telegram.org/bots/api#location
    """

    required = {
        "longitude": float,
        "latitude": float,
    }

    def __eq__(self, other):
        return isinstance(other, Location) and \
            self.longitude == other.longitude and \
            self.latitude == other.latitude


class Venue(BaseObject):
    """Telegram API representation of a venue

    https://core.telegram.orgf/bots/api#venue
    """

    required = {
        "location": Location,
        "title": str,
        "address": str,
    }
    optional = {
        "foursquare_id": str,
    }
    replace_keys = {
        "foursquare_id": "foursquare",
    }
    _check_equality_ = "location"
