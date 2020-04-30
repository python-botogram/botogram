# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
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
from datetime import datetime as dt
from time import mktime
from .media import Photo, ChatPhoto


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
        "language_code": str,
        "is_bot": bool,
    }
    replace_keys = {
        "language_code": "lang",
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
        "id": int
    }
    optional = {
        "type": str,
        "title": str,
        "username": str,
        "first_name": str,
        "last_name": str,
        "all_members_are_administrators": bool,
        "description": str,
        "invite_link": str,
        # This is added at the bottom of messages.py due to circular imports
        # "pinned_message" = Message
        "sticker_set_name": str,
        "can_set_sticker_set": bool,
        "photo": ChatPhoto,
    }
    replace_keys = {
        "invite_link": "_invite_link",
        "photo": "_photo",
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

    def kick(self, user, time=None):
        if self.type == "private":
            raise RuntimeError("This chat is a private!")
        if isinstance(user, User):
            user = user.id

        if time is None:
            self._api.call("unbanChatMember", {
                "chat_id": self.id,
                "user_id": user
            })
        else:
            if isinstance(time, dt):
                time = mktime(time.timetuple())
            self._api.call("kickChatMember", {
                "chat_id": self.id,
                "user_id": user,
                "until_date": time
            })

    def permissions(self, user):
        return Permissions(user, self)

    def set_description(self, description=""):
        if self.type != "private":
            """Set the new chat description. Leave empty to delete it."""
            if len(description) <= 255:
                self._api.call("setChatDescription", {
                    "chat_id": self.id,
                    "description": description
                }, expect=bool)
            else:
                raise ValueError("The new description must be below 255 characters.")
        else:
            raise RuntimeError("This method works only with non-private chats.")

    @mixins._require_api
    def revoke_invite_link(self):
        """Revoke and generate a new invike link for this chat"""
        if self.type not in ("supergroup", "channel"):
            raise RuntimeError("You can revoke the invite link only in a supergroup or a channel")

        link = self._api.call("exportChatInviteLink", {
            "chat_id": self.id,
        }).get('result', None)
        self._cache_invite_link = link
        return link

    @property
    @mixins._require_api
    def invite_link(self):
        """Get the invite link of this chat"""
        if self.type not in ("supergroup", "channel"):
            raise RuntimeError("You can get the invite link only in a supergroup or a channel")

        if hasattr(self, "_cache_invite_link"):
            return self._cache_invite_link

        chat = self._api.call("getChat", {
            "chat_id": self.id,
        }, expect=Chat)
        if not chat._invite_link:
            return self.revoke_invite_link()

        self._cache_invite_link = chat._invite_link
        return self._cache_invite_link

    def pin_message(self, message, notify=True):
        """Pin a message"""
        # Check if the chat is a supergroup
        if self.type not in ("supergroup", "channel"):
            raise RuntimeError("This chat is nota a supergroup or channel!")

        if isinstance(message, Message):
            message = message.id

        return self._api.call("pinChatMessage", {
            "chat_id": self.id,
            "message_id": message,
            "disable_notification": not notify
        }, expect=bool)

    @property
    @mixins._require_api
    def photo(self):
        """Get the current chat photo small and big ids"""
        if hasattr(self, "_cache_photo"):
            return self._cache_photo

        if self._photo is not None:
            self._cache_photo = self._photo
            return self._cache_photo

        chat = self._api.call("getChat", {
            "chat_id": self.id
        }, expect=Chat)
        if not chat._photo:
            raise RuntimeError("This chat doesn't have a photo")

        self._cache_photo = chat._photo
        return self._cache_photo

    def unpin_message(self):
        return self._api.call("unpinChatMessage", {
            "chat_id": self.id,
        }, expect=bool)


class Permissions:
    def __init__(self, user, chat):
        if chat.type not in ("group", "supergroup"):
            raise RuntimeError("This chat is not a group or a supergroup!")
        # Accept also an instance of `User`
        self._chat_id = chat.id
        self._api = chat._api
        if isinstance(user, User):
            self._user = user.id
        else:
            self._user = user
        infouser = self._api.call("getChatMember", {
            "chat_id": self._chat_id,
            "user_id": self._user},
                                  expect=ChatMember)

        try:
            self._until_date = infouser.until_date
        except AttributeError:
            self._until_date = 0
        self.until_date = self._until_date

        try:
            self._send_messages = infouser.can_send_messages
        except AttributeError:
            self._send_messages = True
        self.send_messages = self._send_messages

        try:
            self._send_media_messages = infouser.can_media_messages
        except AttributeError:
            self._send_media_messages = True
        self.send_media_messages = self._send_media_messages

        try:
            self._send_other_messages = infouser.can_send_other_messages
        except AttributeError:
            self._send_other_messages = True
        self.send_other_messages = self._send_other_messages

        try:
            self._add_web_page_previews = infouser.can_add_web_page_previews
        except AttributeError:
            self._add_web_page_previews = True
        self.add_web_page_previews = self._add_web_page_previews

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.save()

    def save(self):
        arguments = {
            "chat_id": self._chat_id,
            "user_id": self._user,
        }
        modify = False

        if isinstance(self.until_date, dt):
            self.until_date = mktime(self.until_date.timetuple())
            modify = True
        if self._until_date != self.until_date:
            arguments.update({"until_date": self.until_date})
            modify = True
        if self._send_messages != self.send_messages:
            arguments.update({"can_send_messages": self.send_messages})
            modify = True
        if self._send_media_messages != self.send_media_messages:
            arguments.update({"can_send_media_messages":
                             self.send_media_messages})
            modify = True
        if self._send_other_messages != self.send_other_messages:
            arguments.update({"can_send_other_messages":
                             self.send_other_messages})
            modify = True
        if self._add_web_page_previews != self.add_web_page_previews:
            arguments.update({"can_add_web_page_previews":
                             self.add_web_page_previews})
            modify = True

        if modify:
            self._api.call("restrictChatMember", arguments)


class ChatMember(BaseObject):
    """Telegram API representation of a chat member

    https://core.telegram.org/bots/api#chatmember
    """

    required = {
        "user": User,
        "status": str,
    }
    optional = {
        "until_date": int,
        "can_be_edited": bool,
        "can_change_info": bool,
        "can_post_messages": bool,
        "can_edit_messages": bool,
        "can_delete_messages": bool,
        "can_invite_users": bool,
        "can_restrict_members": bool,
        "can_pin_messages": bool,
        "can_promote_members": bool,
        "can_send_messages": bool,
        "can_send_media_messages": bool,
        "can_send_other_messages": bool,
        "can_add_web_page_previews": bool
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


# add this code on the button to avoid import loop
# flake8: noqa
from .messages import Message
Chat.optional["pinned_message"] = Message
