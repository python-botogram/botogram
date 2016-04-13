"""
    botogram.objects.messages
    Representation of messages-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


from .base import BaseObject, _itself
from . import mixins
from .. import utils

from .chats import User, Chat
from .media import Audio, Voice, Document, Photo, Sticker, Video, Contact, \
                   Location


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
        "new_chat_member": User,
        "left_chat_member": User,
        "new_chat_title": str,
        "new_chat_photo": Photo,
        "delete_chat_photo": bool,
        "group_chat_created": bool,
        "supergroup_chat_created": bool,
        "channel_chat_created": bool,
        "migrate_to_chat_id": int,
        "migrate_from_chat_id": int,
        "pinned_message": _itself,
    }
    replace_keys = {
        "from": "sender",
    }

    @property
    @utils.deprecated("Message.new_chat_participant", "1.0",
                      "Rename property to Message.new_chat_member")
    def new_chat_participant(self):
        return self.new_chat_member

    @property
    @utils.deprecated("Message.left_chat_participant", "1.0",
                      "Rename property ot Message.left_chat_member")
    def left_chat_participant(self):
        return self.left_chat_member
