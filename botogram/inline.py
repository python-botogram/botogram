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
from . import syntaxes


class Inline:

    @staticmethod
    def article(title, text, syntax=None, preview=True, attach=None):
        args = {"type": "article",
                "id": None,
                "title": title,
                "input_message_content": {
                    "message_text": text,
                    "disable_web_page_preview": not preview
                }
                }
        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = \
                attach._serialize_attachment("-100200000")
        syntax = syntaxes.guess_syntax(text, syntax)
        if syntax is not None:
            args["input_message_content"]["parse_mode"] = syntax
        return args


def process(bot, chains, update):
    """Process a message sent to the bot"""
    for hook in chains["inline"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)

        if result is True:
            bot.logger.debug("Update #%s was just processed by the %s hook."
                             % (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)
