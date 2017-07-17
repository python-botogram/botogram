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

import re

from .base import BaseObject, _itself
from . import mixins
from .. import utils

from .chats import User, Chat
from .media import Audio, Voice, Document, Photo, Sticker, Video, Contact, \
    Location, Venue


_url_protocol_re = re.compile(r"^https?:\/\/|s?ftp:\/\/|mailto:", re.I)


def _require_message(func):
    """Decorator which forces the object to have an attached message"""
    @utils.wraps(func)
    def __(self, *args, **kwargs):
        if not hasattr(self, "_message") or self._message is None:
            raise RuntimeError("A message must be attached to this object")
        return func(self, *args, **kwargs)
    return __


class ParsedTextEntity(BaseObject):
    """Telegram API representation of an entity in a text message

    This was originally called MessageEntity by Telegram
    https://core.telegram.org/bots/api#messageentity
    """

    required = {
        "type": str,
        "offset": int,
        "length": int,
    }
    optional = {
        "url": str,
        "user": User,
    }
    replace_keys = {
        "url": "_url",  # Dynamically implemented
        "type": "_type",  # Dynamically implemented

        # Private attributes, use the ``text`` one
        "offset": "_offset",
        "length": "_length",
    }

    # Bring some sanity to the Bot API
    replace_types = {
        "bot_command": "command",
        "text_link": "link",
        "url": "link",
        "text_mention": "mention",
    }
    replace_types_inverse = {
        "command": "bot_command",
        "link": "text_link",
        "mention": "text_mention",
    }

    def __init__(self, data, api=None, message=None):
        super().__init__(data, api)

        self._message = message

    def __eq__(self, other):
        if not isinstance(other, ParsedTextEntity):
            return False

        # Don't do custom equality if no message object is attached
        if self._message is None or other._message is None:
            return id(self) == id(other)

        return self._message.message_id == other._message.message_id and \
            self._offset == other._offset and self._length == other._length

    def __str__(self):
        return self.text

    def __repr__(self):
        if self._message is not None:
            return '<ParsedTextEntity %s: "%s">' % (self.type, self.text)
        else:
            return '<ParsedTextEntity %s from %s to %s>' % (
                self.type,
                self._offset,
                self._offset + self._length
            )

    def __len__(self):
        return self._length

    def set_message(self, message):
        """Set the message instance related to this object"""
        self._message = message

    @property
    def type(self):
        """Get the type of the entity"""
        # Bring some sanity to the Bot API
        if self._type in self.replace_types:
            return self.replace_types[self._type]
        return self._type

    @type.setter
    def type(self, value):
        """Set the type of the entity"""
        # Special check for link, because two original types points to it
        if value == "link":
            # If the URL is not set or it's the same as the text, then it's a
            # normal URL, else it has a label
            if self.text == self._url or self._url is None:
                self._type = "url"
            else:
                self._type = "text_link"

        elif value == "mention":
            if self.user is not None:
                self._type = "text_mention"
            else:
                self._type = "mention"

        elif value in self.replace_types_inverse:
            self._type = self.replace_types_inverse[value]
        else:
            self._type = value

    @property
    @_require_message
    def text(self):
        """Get the text of the message"""
        if self._message.text is None:
            raise ValueError("The message must have a text")

        start = self._offset
        stop = start + self._length

        if stop > len(self._message.text):
            raise ValueError("The message is too short!")

        return self._message.text[start:stop]

    @property
    @_require_message
    def url(self):
        """Get the URL attached to the message"""
        if self._url is not None:
            # Use the provided if available
            url = self._url
        elif self.type == "link":
            # Standard URLs
            url = self.text
        elif self.type == "mention":
            # Detect the correct username
            if self.user is not None and self.user.username is not None:
                username = self.user.username
            elif self.text.startswith("@"):
                username = self.text[1:]
            else:
                return None

            # telegram.me URLs
            return "https://telegram.me/%s" % username
        elif self.type == "email":
            # mailto: URL
            return "mailto:%s" % self.text
        else:
            # Sorry!
            return None

        # Be sure to have a protocol in the URL (default to HTTP)
        # Apparently Telegram doesn't provide always a valid URL, but whatever
        # the user sends in the message
        if not _url_protocol_re.match(url):
            url = "http://%s" % url
        return url


class ParsedText:
    """Collection of ParsedTextEntity.

    This is a list-like object, and mimics the List<MessageEntity> Telegram
    object, but increases its functionalities.
    """

    def __init__(self, data, api=None, message=None):
        self._api = api
        # Accept only list of entites
        if not isinstance(data, list):
            raise ValueError("You must provide a list of ParsedTextEntity")

        # Create ParsedTextEntity instances from the data
        self._original_entities = []
        for entity in data:
            parsed = ParsedTextEntity(entity, api, message)
            self._original_entities.append(parsed)

        # Original entities are separated from the exposed entities because
        # plaintext entities are calculated and added to the exposend entities
        self._entities = None

        self.set_message(message)

    def __eq__(self, other):
        return isinstance(other, ParsedText) and \
            self._entities == other._entities

    def __repr__(self):
        return '<ParsedText %s>' % repr(self._calculate_entities())

    def set_api(self, api):
        """Change the API instance"""
        self._api = api

    def set_message(self, message):
        """Change the message instance"""
        if message is not None and message.text is None:
            raise ValueError("The message must have some text")

        self._message = message
        for entity in self._original_entities:
            entity.set_message(message)

        # Refresh the calculated entities list
        self._entities = None

    def serialize(self):
        """Serialize this object"""
        result = []
        for entity in self._original_entities:
            result.append(entity.serialize())

        return result

    @_require_message
    def _calculate_entities(self):
        """Calculate the correct list of entities"""
        # Return the cached result if possible; the cached result is nullified
        # when a new instance of Message is attached
        if self._entities is not None:
            return self._entities

        offset = 0
        self._entities = []
        for entity in self._original_entities:
            # If there was some text before the current entity, add an extra
            # plaintext entity
            if offset < entity._offset:
                self._entities.append(ParsedTextEntity({
                    "type": "plain",
                    "offset": offset,
                    "length": entity._offset - offset,
                }, self._api, self._message))

            self._entities.append(entity)
            offset = entity._offset + entity._length

        # Then add the last few bits as plaintext if they're present
        if offset < len(self._message.text):
            self._entities.append(ParsedTextEntity({
                "type": "plain",
                "offset": offset,
                "length": len(self._message.text) - offset,
            }, self._api, self._message))

        return self._entities

    def filter(self, *types, exclude=False):
        """Get only some types of entities"""
        result = []
        for entity in self._calculate_entities():
            # If the entity type is in the allowed ones and exclude is False OR
            # if the entity type isn't in the allowed ones and exclude is True
            if (entity.type in types) ^ exclude:
                result.append(entity)

        return result

    # Provide a basic list-like interface; you can always mutate this object to
    # a list with list(self) if you need more advanced methods

    def __iter__(self):
        return iter(self._calculate_entities())

    def __getitem__(self, index):
        return self._calculate_entities()[index]

    def __contains__(self, key):
        # This checks if a given type is in the entities list
        return key in (entity.type for entity in self._entities)


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
        "date": int,
        "chat": Chat,
    }
    optional = {
        "from": User,
        "entities": ParsedText,
        "forward_from": User,
        "forward_from_chat": Chat,
        "forward_from_message_id": int,
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
        "venue": Venue,
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
        "edit_date": int,
    }
    replace_keys = {
        "from": "sender",
        "entities": "parsed_text",

        # Those are provided dynamically by self.forward_from
        "forward_from": "_forward_from",
        "forward_from_chat": "_forward_from_chat",
    }
    _check_equality_ = "message_id"

    def __init__(self, data, api=None):
        super().__init__(data, api)

        # Create the parsed_text instance even if there are no entities in the
        # current text
        if self.text is not None and self.parsed_text is None:
            self.parsed_text = ParsedText([], api, self)

        # Be sure to set this as the Message instance in the parsed text
        # The instance is needed to calculate the content of each entity
        if self.parsed_text is not None:
            self.parsed_text.set_message(self)

    @property
    def forward_from(self):
        """Get from where the message was forwarded"""
        # Provide either _forward_from or _forward_from_chat
        # _forward_from_chat is checked earlier because it's more correct
        if self._forward_from_chat is not None:
            return self._forward_from_chat

        if self._forward_from is not None:
            return self._forward_from

    @property
    def channel_post_author(self):
        """Get the author of the channel post"""
        if self.chat.type == "channel":
            return self.sender

        if self._forward_from_chat is not None:
            if self.forward_from.type == "channel":
                return self._forward_from

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
