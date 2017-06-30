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

from .. import api
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
    _check_equality_ = "id"

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
    _check_equality_ = "id"

    def _to_user(self):
        """Convert this Chat object to an User object"""
        if self.type != "private":
            raise TypeError("This method works only on private chats!")

        # Be sure to cache the instance
        if not hasattr(self, "_cache_user"):
            self._cache_user = User({
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
            }, self._api)

        return self._cache_user

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

    @property
    def admins(self):
        """Get a list of the admins of the chat"""
        # If this is a private chat, return the current user since Telegram
        # doesn't support `getChatAdministrators` for private chats
        if self.type == "private":
            return [self._to_user()]
        elif self.type == "channel":
            raise TypeError("Not available on channels")

        # Be sure to cache the list of the admins
        if not hasattr(self, "_cache_admins"):
            members = self._api.call("getChatAdministrators",
                                     {"chat_id": self.id},
                                     expect=multiple(ChatMember))
            self._cache_admins = tuple(member.user for member in members)

        # The list of admins is saved as a tuple, so it's not mutable, but it's
        # returned as a list (the tuple thing is an implementation detail)
        return list(self._cache_admins)

    @property
    def creator(self):
        """Get the creator of this chat"""
        # If this is a private chat, return the current user since Telegram
        # doesn't support `getChatAdministrators` for private chats
        if self.type == "private":
            return self._to_user()
        elif self.type == "channel":
            raise TypeError("Not available on channels")

        # Be sure to cache the chat creator
        if not hasattr(self, "_cache_creator"):
            # Get a list of the admins and fetch only the creator
            members = self._api.call("getChatAdministrators",
                                     {"chat_id": self.id},
                                     expect=multiple(ChatMember))
            self._cache_creator = [member.user for member in members
                                   if member.status == "creator"][0]

        return self._cache_creator

    @property
    def members_count(self):
        """Get the number of members of this chat"""
        # This isn't *really* needed, but avoids an HTTP request
        if self.type == "private":
            return 1

        # Be sure to cache the number of members
        if not hasattr(self, "_cache_members_count"):
            self._cache_members_count = self._api.call("getChatMembersCount",
                                                       {"chat_id": self.id},
                                                       expect=int)
        return self._cache_members_count

    def status_of(self, user):
        """Check the status of a member of the group"""
        if self.type in ("private", "channel"):
            raise TypeError("Not available in private chats or channels")

        # Convert Users to IDs
        if isinstance(user, User):
            user = user.id

        # Initialize the cache
        if not hasattr(self, "_cache_status_of"):
            self._cache_status_of = {}

        # Populate the cache for new users
        if user not in self._cache_status_of:
            member = self._api.call("getChatMember", {
                "chat_id": self.id,
                "user_id": user,
            }, expect=ChatMember)
            self._cache_status_of[user] = member.status

        return self._cache_status_of[user]

    def leave(self):
        """Leave this chat"""
        if self.type not in ("group", "supergroup"):
            raise TypeError("This method can only be called in groups and "
                            "supergroups")

        try:
            self._api.call("leaveChat", {"chat_id": self.id})
        except api.APIError as e:
            if e.error_code == 403 and "not a member" in e.description:
                exc = RuntimeError("The bot isn't a member of this group")
                raise exc from None
            raise

    @mixins._require_api
    def ban(self, user):
        """Ban an user from the group"""
        # Check if the chat is a group
        if self.type not in ("group", "supergroup"):
            raise RuntimeError("This chat is not a group or a supergroup!")

        # Accept also an instance of `User`
        if isinstance(user, User):
            user = user.id

        self._api.call("kickChatMember", {
            "chat_id": self.id,
            "user_id": user,
        })

    @mixins._require_api
    def unban(self, user):
        """Unban an user from the supergroup"""
        # Check if the chat is a supergroup
        if self.type != "supergroup":
            raise RuntimeError("This chat is nota group or a supergroup!")

        # Accept also an instance of `User`
        if isinstance(user, User):
            user = user.id

        self._api.call("unbanChatMember", {
            "chat_id": self.id,
            "user_id": user,
        })


class ChatMember(BaseObject):
    """Telegram API representation of a chat member

    https://core.telegram.org/bots/api#chatmember
    """

    required = {
        "user": User,
        "status": str,
    }
    _check_equality_ = "user"


class UserProfilePhotos(BaseObject):
    """Telegram API representation of an user's profile photos

    https://core.telegram.org/bots/api#userprofilephotos
    """

    required = {
        "total_count": int,
        "photos": multiple(Photo),
    }
