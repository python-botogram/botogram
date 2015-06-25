"""
    botogram.objects
    Representation of the different upstream API objects

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
                    print(field_type, hasattr(field_type, "_provide_api"))
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


### Actual objects ###


class EmptyObject(BaseObject):
    """Just an empty object"""
    pass


class User(BaseObject):
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


class GroupChat(BaseObject):
    """Telegram API representation of a group chat

    https://core.telegram.org/bots/api#groupchat
    """

    required = {
        "id": int,
        "title": str,
    }


class PhotoSize(BaseObject):
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


class Audio(BaseObject):
    """Telegram API representation of an audio message

    https://core.telegram.org/bots/api#audio
    """

    required = {
        "file_id": str,
        "duration": int,
    }
    optional = {
        "mime_type": str,
        "file_size": int,
    }


class Document(BaseObject):
    """Telegram API representation of a document

    https://core.telegram.org/bots/api#document
    """

    required = {
        "file_id": str,
        "thumb": one_of(PhotoSize, EmptyObject),
    }
    optional = {
        "file_name": str,
        "mime_type": str,
        "file_size": str,
    }


class Sticker(BaseObject):
    """Telegram API representation of a sticker

    https://core.telegram.org/bots/api#sticker
    """

    required = {
        "file_id": str,
        "width": int,
        "height": int,
        "thumb": one_of(PhotoSize, EmptyObject),
    }
    optional = {
        "file_size": int,
    }


class Video(BaseObject):
    """Telegram API representation of a video

    https://core.telegram.org/bots/api#video
    """

    required = {
        "file_id": str,
        "width": int,
        "height": int,
        "duration": int,
        "thumb": one_of(PhotoSize, EmptyObject),
    }
    optional = {
        "mime_type": str,
        "file_size": int,
        "caption": int,
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
        "user_id": str,
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
        "photos": multiple(multiple(one_of(PhotoSize, EmptyObject))),
    }


class Message(BaseObject):
    """Telegram API representation of a message

    https://core.telegram.org/bots/api#message
    """

    required = {
        "message_id": int,
        "from": User,
        "date": int,
        "chat": one_of(User, GroupChat),
    }
    optional = {
        "forward_from": User,
        "forward_date": int,
        "reply_to_message": _itself,
        "text": str,
        "audio": Audio,
        "document": Document,
        "photo": multiple(PhotoSize),
        "sticker": Sticker,
        "video": Video,
        "contact": Contact,
        "location": Location,
        "new_chat_participant": User,
        "left_chat_participant": User,
        "new_chat_title": str,
        "new_chat_photo": multiple(PhotoSize),
        "delete_chat_photo": bool,
        "group_chat_crated": bool,
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

    https://core.elegram.org/bots/api#forcereply
    """

    required = {
        "force_reply": bool,
    }
    optional = {
        "selective": bool,
    }
