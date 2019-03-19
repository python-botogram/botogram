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

# flake8: noqa

from .chats     import User, Chat, UserProfilePhotos, Permissions
from .media     import PhotoSize, Photo, Audio, Voice, Document, Sticker, \
                       Video, VideoNote, Contact, Location, Venue
from .messages  import Message
from .markup    import ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply
from .updates   import Update, Updates
from .mixins import Album

__all__ = [
    # Chats-related objects
    "User",
    "Chat",
    "UserProfilePhotos",

    # Media-related objects
    "PhotoSize",
    "Photo",
    "Audio",
    "Voice",
    "Document",
    "Sticker",
    "Video",
    "VideoNote",
    "Contact",
    "Location",
    "Venue",
    "Album",

    # Messages-related objects
    "Message",

    # Markup-related objects
    "ReplyKeyboardMarkup",
    "ReplyKeyboardHide",
    "ForceReply",

    # Updates-related objects
    "Update",
    "Updates",
]
