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


def process_message(bot, chains, update):
    """Process a message sent to the bot"""
    for hook in chains["messages"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update #%s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


def process_edited_message(bot, chains, update):
    """Process an edited message"""
    for hook in chains["messages_edited"]:
        bot.logger.debug("Processing edited message in update #%s with the "
                         "hook %s..." % (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update %s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


def process_channel_post(bot, chains, update):
    """Process a channel post"""
    for hook in chains["channel_post"]:
        bot.logger.debug("Processing channel post in update #%s with the "
                         "hook %s..." % (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update %s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


def process_channel_post_edited(bot, chains, update):
    """Process an edited channel post"""
    for hook in chains["channel_post_edited"]:
        bot.logger.debug("Processing edited channel post in update #%s with"
                         "the hook %s..." % (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update %s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)
