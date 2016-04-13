"""
    botogram.objects.chats
    Representation of the chat-related upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .base import BaseObject, multiple
from . import mixins

from .media import Photo


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


class UserProfilePhotos(BaseObject):
    """Telegram API representation of an user's profile photos

    https://core.telegram.org/bots/api#userprofilephotos
    """

    required = {
        "total_count": int,
        "photos": multiple(Photo),
    }
