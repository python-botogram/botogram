# Copyright (c) 2015-2020 The Botogram Authors (see AUTHORS)
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

from . import syntaxes


def process(bot, chains, update):
    """Process an inline update"""
    for hook in chains["inline"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is {'ok': True, 'result': True}:
            bot.logger.debug("Update #%s was just processed by the %s hook."
                             % (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


def inline_feedback_process(bot, chains, update):
    """Process a chosen inline result update"""
    for hook in chains["inline_feedback"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is {'ok': True}:
            bot.logger.debug("Update #%s was just processed by the %s hook."
                             % (update.update_id, hook.name))
            return
    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


class InlineInputMessage:
    """A factory for InputMessageContent Telegram objects"""

    def __init__(self, text, syntax=None, preview=True):
        self.text = text
        self.syntax = syntax
        self.preview = preview

    def _serialize(self):
        args = {
            "message_text": self.text,
            "disable_web_page_preview": not self.preview,
        }
        syntax = syntaxes.guess_syntax(self.text, self.syntax)
        if syntax:
            args["parse_mode"] = syntax
        return args


class InlineInputLocation:
    """A factory for InputLocationMessageContent Telegram objects"""

    def __init__(self, latitude, longitude, live_period=None):
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period

    def _serialize(self):
        args = {
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
        if self.live_period is not None:
            args["live_period"] = self.live_period
        return args


class InlineInputVenue:
    """A factory for InputVenueMessageContent Telegram objects"""

    def __init__(self, latitude, longitude, title, address,
                 foursquare_id=None, foursquare_type=None):
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type

    def _serialize(self):
        args = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "title": self.title,
            "address": self.address,
        }
        if self.foursquare_id is not None:
            args["foursquare_id"] = self.foursquare_id
            if self.foursquare_type is not None:
                args["foursquare_type"] = self.foursquare_type
        return args


class InlineInputContact:
    """A factory for InputContactMessageContent Telegram objects"""

    def __init__(self, phone, first_name, last_name=None, vcard=None):
        self.phone_number = phone
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard

    def _serialize(self):
        args = {
            "phone_number": self.phone_number,
            "first_name": self.first_name,
        }
        if self.last_name is not None:
            args["last_name"] = self.last_name
        if self.vcard is not None:
            args["vcard"] = self.vcard
        return args
