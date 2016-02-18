"""
    botogram.objects.mixins
    Additional management methods for upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .. import utils
from .. import syntaxes


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

    def _get_call_args(self, reply_to, extra):
        """Get default API call arguments"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Get the correct chat_id
        # There is an hasattr because User objects doesn't have any type
        if hasattr(self, "type"):
            chat_id = self.username if self.type == "channel" else self.id
        else:
            chat_id = self.id

        args = {"chat_id": chat_id}
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        return args

    @_require_api
    def send(self, message, preview=True, reply_to=None, syntax=None,
             extra=None):
        """Send a message"""
        args = self._get_call_args(reply_to, extra)
        args["text"] = message
        args["disable_web_page_preview"] = not preview

        syntax = syntaxes.guess_syntax(message, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        self._api.call("sendMessage", args)

    @_require_api
    def send_photo(self, path, caption=None, reply_to=None, extra=None):
        """Send a photo"""
        args = self._get_call_args(reply_to, extra)
        if caption is not None:
            args["caption"] = caption

        files = {"photo": open(path, "rb")}
        self._api.call("sendPhoto", args, files)

    @_require_api
    def send_audio(self, path, duration=None, performer=None, title=None,
                   reply_to=None, extra=None):
        """Send an audio track"""
        args = self._get_call_args(reply_to, extra)
        if duration is not None:
            args["duration"] = duration
        if performer is not None:
            args["performer"] = performer
        if title is not None:
            args["title"] = title

        files = {"audio": open(path, "rb")}
        self._api.call("sendAudio", args, files)

    @_require_api
    def send_voice(self, path, duration=None, title=None, reply_to=None,
                   extra=None):
        """Send a voice message"""
        args = self._get_call_args(reply_to, extra)
        if duration is not None:
            args["duration"] = duration

        files = {"voice": open(path, "rb")}
        self._api.call("sendVoice", args, files)

    @_require_api
    def send_video(self, path, duration=None, caption=None, reply_to=None,
                   extra=None):
        """Send a video"""
        args = self._get_call_args(reply_to, extra)
        if duration is not None:
            args["duration"] = duration
        if caption is not None:
            args["caption"] = caption

        files = {"video": open(path, "rb")}
        self._api.call("sendVideo", args, files)

    @_require_api
    def send_file(self, path, reply_to=None, extra=None):
        """Send a generic file"""
        args = self._get_call_args(reply_to, extra)

        files = {"document": open(path, "rb")}
        self._api.call("sendDocument", args, files)

    @_require_api
    def send_location(self, latitude, longitude, reply_to=None, extra=None):
        """Send a geographic location"""
        args = self._get_call_args(reply_to, extra)
        args["latitude"] = latitude
        args["longitude"] = longitude

        self._api.call("sendLocation", args)


class MessageMixin:
    """Add some methods for messages"""

    @_require_api
    def forward_to(self, to):
        """Forward the message to another user"""
        if hasattr(to, "id"):
            to = to.id

        self._api.call("forwardMessage", {
            "chat_id": to,
            "from_chat_id": self.chat.id,
            "message_id": self.message_id,
        })

    @_require_api
    def reply(self, message, preview=True, syntax=None, extra=None):
        """Reply to the current message"""
        self.chat.send(message, preview, self.message_id, syntax, extra)

    @_require_api
    def reply_with_photo(self, path, caption=None, extra=None):
        """Reply with a photo to the current message"""
        self.chat.send_photo(path, caption, self.message_id, extra)

    @_require_api
    def reply_with_audio(self, path, duration=None, performer=None, title=None,
                         extra=None):
        """Reply with an audio track to the current message"""
        self.chat.send_audio(path, duration, performer, title, self.message_id,
                             extra)

    @_require_api
    def reply_with_voice(self, path, duration=None, extra=None):
        """Reply with a voice message to the current message"""
        self.chat.send_voice(path, duration, self.message_id, extra)

    @_require_api
    def reply_with_video(self, path, duration=None, caption=None, extra=None):
        """Reply with a video to the current message"""
        self.chat.send_video(path, duration, caption, self.message_id, extra)

    @_require_api
    def reply_with_file(self, path, extra=None):
        """Reply with a generic file to the current chat"""
        self.chat.send_file(path, self.message_id, extra)

    @_require_api
    def reply_with_location(self, latitude, longitude, extra=None):
        """Reply with a geographic location to the current chat"""
        self.chat.send_location(latitude, longitude, self.message_id, extra)


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
