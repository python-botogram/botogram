"""
    botogram.messages
    Logic for processing messages sent to your bot

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


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
