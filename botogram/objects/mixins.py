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

import importlib
import json

from .. import utils
from .. import syntaxes


_objects_module = None


def _objects():
    global _objects_module

    # This is lazily loaded to avoid circular dependencies
    if _objects_module is None:
        _objects_module = importlib.import_module("..objects", __package__)

    return _objects_module


def _require_api(func):
    """Decorator which forces to have the api on an object"""
    @utils.wraps(func)
    def __(self, *args, **kwargs):
        if not hasattr(self, "_api") or self._api is None:
            raise RuntimeError("An API instance must be provided")
        return func(self, *args, **kwargs)
    return __


class ChatMixin:
    """Add some methods for chats"""

    def _get_call_args(self, reply_to, extra, notify=True):
        """Get default API call arguments"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        args = {"chat_id": self.id}
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = json.dumps(extra.serialize())
        if not notify:
            args["disable_notification"] = True

        return args

    @_require_api
    def send(self, message, preview=True, reply_to=None, syntax=None,
             extra=None, notify=True):
        """Send a message"""
        args = self._get_call_args(reply_to, extra, notify)
        args["text"] = message
        args["disable_web_page_preview"] = not preview

        syntax = syntaxes.guess_syntax(message, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        return self._api.call("sendMessage", args, expect=_objects().Message)

    @_require_api
    def send_photo(self, path, caption=None, reply_to=None, extra=None,
                   notify=True):
        """Send a photo"""
        args = self._get_call_args(reply_to, extra, notify)
        if caption is not None:
            args["caption"] = caption

        files = {"photo": open(path, "rb")}

        return self._api.call("sendPhoto", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_audio(self, path, duration=None, performer=None, title=None,
                   reply_to=None, extra=None, notify=True):
        """Send an audio track"""
        args = self._get_call_args(reply_to, extra, notify)
        if duration is not None:
            args["duration"] = duration
        if performer is not None:
            args["performer"] = performer
        if title is not None:
            args["title"] = title

        files = {"audio": open(path, "rb")}

        return self._api.call("sendAudio", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_voice(self, path, duration=None, title=None, reply_to=None,
                   extra=None, notify=True):
        """Send a voice message"""
        args = self._get_call_args(reply_to, extra, notify)
        if duration is not None:
            args["duration"] = duration

        files = {"voice": open(path, "rb")}

        return self._api.call("sendVoice", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_video(self, path, duration=None, caption=None, reply_to=None,
                   extra=None, notify=True):
        """Send a video"""
        args = self._get_call_args(reply_to, extra, notify)
        if duration is not None:
            args["duration"] = duration
        if caption is not None:
            args["caption"] = caption

        files = {"video": open(path, "rb")}

        return self._api.call("sendVideo", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_file(self, path, reply_to=None, extra=None, notify=True):
        """Send a generic file"""
        args = self._get_call_args(reply_to, extra, notify)

        files = {"document": open(path, "rb")}

        return self._api.call("sendDocument", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_location(self, latitude, longitude, reply_to=None, extra=None,
                      notify=True):
        """Send a geographic location"""
        args = self._get_call_args(reply_to, extra, notify)
        args["latitude"] = latitude
        args["longitude"] = longitude

        return self._api.call("sendLocation", args,
                              expect=_objects().Message)

    @_require_api
    def send_venue(self, latitude, longitude, title, address, foursquare=None,
                   reply_to=None, extra=None, notify=True):
        """Send a venue"""
        args = self._get_call_args(reply_to, extra, notify)
        args["latitude"] = latitude
        args["longitude"] = longitude
        args["title"] = title
        args["address"] = address
        if foursquare is not None:
            args["foursquare_id"] = foursquare

        self._api.call("sendVenue", args, expect=_objects().Message)

    @_require_api
    def send_sticker(self, sticker, reply_to=None, extra=None, notify=True):
        """Send a sticker"""
        args = self._get_call_args(reply_to, extra, notify)

        files = {"sticker": open(sticker, "rb")}
        return self._api.call("sendSticker", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_contact(self, phone, first_name, last_name=None, *, reply_to=None,
                     extra=None, notify=True):
        """Send a contact"""
        args = self._get_call_args(reply_to, extra, notify)
        args["phone_number"] = phone
        args["first_name"] = first_name

        if last_name is not None:
            args["last_name"] = last_name

        return self._api.call("sendContact", args, expect=_objects().Message)

    @_require_api
    def delete_message(self, message):
        """Delete a message from chat"""
        if hasattr(message, "message_id"):
            message = message.message_id

        return self._api.call("deleteMessage", {
            "chat_id": self.id,
            "message_id": message,
        })


class MessageMixin:
    """Add some methods for messages"""

    @_require_api
    def forward_to(self, to, notify=True):
        """Forward the message to another user"""
        if hasattr(to, "id"):
            to = to.id

        args = dict()
        args["chat_id"] = to
        args["from_chat_id"] = self.chat.id
        args["message_id"] = self.message_id
        if not notify:
            args["disable_notification"] = True

        return self._api.call("forwardMessage", args,
                              expect=_objects().Message)

    @_require_api
    def edit(self, text, syntax=None, preview=True, extra=None):
        """Edit this message"""
        args = {"message_id": self.message_id, "chat_id": self.chat.id}
        args["text"] = text

        syntax = syntaxes.guess_syntax(text, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        if not preview:
            args["disable_web_page_preview"] = True
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        self._api.call("editMessageText", args)
        self.text = text

    @_require_api
    def edit_caption(self, caption, extra=None):
        """Edit this message's caption"""
        args = {"message_id": self.message_id, "chat_id": self.chat.id}
        args["caption"] = caption

        if extra is not None:
            args["reply_markup"] = extra.serialize()

        self._api.call("editMessageCaption", args)
        self.caption = caption

    @_require_api
    def reply(self, *args, **kwargs):
        """Reply to the current message"""
        return self.chat.send(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_photo(self, *args, **kwargs):
        """Reply with a photo to the current message"""
        return self.chat.send_photo(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_audio(self, *args, **kwargs):
        """Reply with an audio track to the current message"""
        return self.chat.send_audio(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_voice(self, *args, **kwargs):
        """Reply with a voice message to the current message"""
        return self.chat.send_voice(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_video(self, *args, **kwargs):
        """Reply with a video to the current message"""
        return self.chat.send_video(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_file(self, *args, **kwargs):
        """Reply with a generic file to the current chat"""
        return self.chat.send_file(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_location(self, *args, **kwargs):
        """Reply with a geographic location to the current chat"""
        return self.chat.send_location(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_venue(self, *args, **kwargs):
        """Reply with a venue to the current message"""
        return self.chat.send_venue(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_sticker(self, *args, **kwargs):
        """Reply with a sticker to the current message"""
        return self.chat.send_sticker(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_contact(self, *args, **kwargs):
        """Reply with a contact to the current message"""
        return self.chat.send_contact(*args, reply_to=self, **kwargs)

    @_require_api
    def delete(self):
        """Delete the message"""
        return self._api.call("deleteMessage", {
            "chat_id": self.chat.id,
            "message_id": self.message_id,
        })


class FileMixin:
    """Add some methods for files"""

    @_require_api
    def save(self, path):
        """Save the file to a particular path"""
        response = self._api.call("getFile", {"file_id": self.file_id})

        # Save the file to the wanted path
        downloaded = self._api.file_content(response["result"]["file_path"])
        with open(path, 'wb') as f:
            f.write(downloaded)


class CallbackMixin:
    """Add some methods for callbacks"""

    @_require_api
    def notify(self, text, alert=False, cache_time=0):
        self._api.call("answerCallbackQuery",
                       {"callback_query_id": self.id,
                        "text": text,
                        "show_alert": alert,
                        "cache_time": cache_time})
