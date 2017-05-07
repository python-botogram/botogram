"""
    botogram.messages
    Logic for callbacks sent to your bot

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""


def process_callback(bot, chains, update):
    for hook in chains["callback_query"]:
        bot.logger.debug("Processing callback query in update #%s with the "
                         "hook %s..." % (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update %s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)
