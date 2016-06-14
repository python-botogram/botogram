"""
    botogram.objects
    Representation of the different upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

# flake8: noqa

from .chats     import User, Chat, UserProfilePhotos
from .media     import PhotoSize, Photo, Audio, Voice, Document, Sticker, \
                       Video, Contact, Location, Venue
from .messages  import Message
from .markup    import ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply
from .updates   import Update, Updates


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
    "Contact",
    "Location",
    "Venue",

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
