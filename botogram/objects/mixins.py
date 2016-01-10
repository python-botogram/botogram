"""
    botogram.objects.mixins
    Additional management methods for upstream API objects

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

from .. import utils


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

    @_require_api
    def send(self, message, preview=True, reply_to=None, syntax=None,
             extra=None):
        """Send a message"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Use the correct syntax
        if syntax is None:
            syntax = "markdown" if utils.is_markdown(message) else "plain"
        elif syntax not in ("plain", "markdown"):
            raise ValueError("Invalid syntax type: %s")

        # Get the correct chat_id
        chat_id = self.username if self.type == "channel" else self.id

        # Build API call arguments
        args = {"chat_id": chat_id, "text": message,
                "disable_web_page_preview": not preview}
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()
        if syntax == "markdown":
            args["parse_mode"] = "Markdown"

        self._api.call("sendMessage", args)

    @_require_api
    def send_photo(self, path, caption=None, reply_to=None, extra=None):
        """Send a photo"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Get the correct chat_id
        chat_id = self.username if self.type == "channel" else self.id

        # Build API call arguments
        args = {"chat_id": chat_id}
        if caption is not None:
            args["caption"] = caption
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        files = {"photo": open(path, "rb")}

        self._api.call("sendPhoto", args, files)

    @_require_api
    def send_audio(self, path, duration=None, performer=None, title=None,
                   reply_to=None, extra=None):
        """Send an audio track"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Get the correct chat_id
        chat_id = self.username if self.type == "channel" else self.id

        args = {"chat_id": chat_id}
        if duration is not None:
            args["duration"] = duration
        if performer is not None:
            args["performer"] = performer
        if title is not None:
            args["title"] = title
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        files = {"audio": open(path, "rb")}

        self._api.call("sendAudio", args, files)

    @_require_api
    def send_voice(self, path, duration=None, title=None, reply_to=None,
                   extra=None):
        """Send a voice message"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "message_id"):
            reply_to = reply_to.message_id

        # Get the corret chat_id
        chat_id = self.username if self.type == "channel" else self.id

        args = {"chat_id": chat_id}
        if duration is not None:
            args["duration"] = duration
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            args["reply_markup"] = extra.serialize()

        files = {"voice": open(path, "rb")}

        self._api.call("sendVoice", args, files)


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
