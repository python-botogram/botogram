"""
    botogram.objects
    Representation of the different upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .base import BaseObject, multiple, _itself
from . import mixins
from .. import utils


class User(BaseObject, mixins.ChatMixin):
    """Telegram API representation of an user

    https://core.telegram.org/bots/api#user
    """

    required = {
        "id": int,
        "first_name": str,
    }
    optional = {
        "last_name": str,
        "username": str,
    }

    @property
    def name(self):
        """Get the full name of the user"""
        result = self.first_name
        if self.last_name is not None:
            result += " " + self.last_name

        return result

    @property
    @mixins._require_api
    def avatar(self):
        """Get the avatar of the user"""
        # This is lazy loaded and cached, so it won't affect performances if
        # you don't need avatars
        if not hasattr(self, "_avatar"):
            avatars = self._api.call("getUserProfilePhotos", {
                "user_id": self.id,
                "limit": 1,
            }, expect=UserProfilePhotos)

            # If the user has no avatars just use None
            self._avatar = None
            if len(avatars.photos):
                self._avatar = avatars.photos[0]  # Take the most recent one

        return self._avatar

    @mixins._require_api
    def avatar_history(self):
        """Get all the avatars of the user"""
        avatars = []

        while True:
            chunk = self._api.call("getUserProfilePhotos", {
                "user_id": self.id,
                "offset": len(avatars),
            }, expect=UserProfilePhotos)

            avatars += chunk.photos
            if len(avatars) >= chunk.total_count:
                break

        return avatars


class Chat(BaseObject, mixins.ChatMixin):
    """Telegram API representation of a chat

    https://core.telegram.org/bots/api#chat
    """

    required = {
        "id": int,
        "type": str,
    }
    optional = {
        "title": str,
        "username": str,
        "first_name": str,
        "last_name": str,
    }

    @property
    def name(self):
        """Get the full name of the chat"""
        result = None

        if self.title is not None:
            result = self.title
        elif self.first_name is not None:
            result = self.first_name
            if self.last_name is not None:
                result += " " + self.last_name

        return result


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
        attrs = list(PhotoSize.required.keys()) + list(PhotoSize.optional.keys())
        for attr in attrs:
            setattr(self, attr, getattr(self.biggest, attr))

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
        "file_size": int,
    }


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


class Location(BaseObject):
    """Telegram API representation of a location mark

    https://core.telegram.org/bots/api#location
    """

    required = {
        "longitude": float,
        "latitude": float,
    }


class UserProfilePhotos(BaseObject):
    """Telegram API representation of an user's profile photos

    https://core.telegram.org/bots/api#userprofilephotos
    """

    required = {
        "total_count": int,
        "photos": multiple(Photo),
    }


class Message(BaseObject, mixins.MessageMixin):
    """Telegram API representation of a message

    https://core.telegram.org/bots/api#message
    """

    @property
    @utils.deprecated("Message.from_", "1.0",
                      "Rename property to Message.sender")
    def from_(self):
        return self.sender

    required = {
        "message_id": int,
        "from": User,
        "date": int,
        "chat": Chat,
    }
    optional = {
        "forward_from": User,
        "forward_date": int,
        "reply_to_message": _itself,
        "text": str,
        "audio": Audio,
        "voice": Voice,
        "document": Document,
        "photo": Photo,
        "sticker": Sticker,
        "video": Video,
        "caption": str,
        "contact": Contact,
        "location": Location,
        "new_chat_participant": User,
        "left_chat_participant": User,
        "new_chat_title": str,
        "new_chat_photo": Photo,
        "delete_chat_photo": bool,
        "group_chat_created": bool,
        "supergroup_chat_created": bool,
        "channel_chat_created": bool,
        "migrate_to_chat_id": int,
        "migrate_from_chat_id": int,
    }
    replace_keys = {
        "from": "sender",
    }


class ReplyKeyboardMarkup(BaseObject):
    """Telegram API representation of a custom keyboard

    https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    required = {
        "keyboard": multiple(multiple(str)),
    }
    optional = {
        "resize_keyboard": bool,
        "one_time_keyboard": bool,
        "selective": bool,
    }


class ReplyKeyboardHide(BaseObject):
    """Telegram API special object which hides a custom keyboard

    https://core.telegram.org/bots/api#replykeyboardhide
    """

    required = {
        "hide_keyboard": bool,
    }
    optional = {
        "selective": bool,
    }


class ForceReply(BaseObject):
    """Telegram API special object which forces the user to reply to a message

    https://core.telegram.org/bots/api#forcereply
    """

    required = {
        "force_reply": bool,
    }
    optional = {
        "selective": bool,
    }


class Update(BaseObject):
    """Telegram API representation of an update

    https://core.telegram.org/bots/api#update
    """

    required = {
        "update_id": int,
    }
    optional = {
        "message": Message
    }


# Shortcut for the Updates type
Updates = multiple(Update)
