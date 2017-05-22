"""
    botogram.objects.payments
    Logic to processing shipping and pre checkout queries sent to your bot

    Copyright (c) 2017 Marco Aceti <dev@marcoaceti.it>
    Released under the MIT license
"""

import json


def process_shipping_query(bot, chains, update):
    """Process a message sent to the bot"""
    for hook in chains["shipping_query"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update #%s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


def process_pre_checkout_query(bot, chains, update):
    """Process a message sent to the bot"""
    for hook in chains["pre_checkout_query"]:
        bot.logger.debug("Processing update #%s with the hook %s..." %
                         (update.update_id, hook.name))

        result = hook.call(bot, update)
        if result is True:
            bot.logger.debug("Update #%s was just processed by the %s hook." %
                             (update.update_id, hook.name))
            return

    bot.logger.debug("No hook actually processed the #%s update." %
                     update.update_id)


class Prices:
    """
    Prices object
    """
    def __init__(self):
        """Create a price object"""
        self._prices = []

    def add(self, label, amount):
        self._prices.append({"label": label, "amount": amount})

    def _to_json(self):
        return json.dumps(self._prices)


class ShippingOptions:
    """
    Shipping options object
    """
    def __init__(self):
        """Create a shipping options object"""
        self._options = []

    def add(self, title, prices):
        """Add a options to options"""
        telegram_prices = []
        for price in prices:
            telegram_prices.append({"label": price, "amount": prices[price]})

        self._options.append({"title": title, "prices": telegram_prices})

    def _to_json(self):
        return json.dumps(self._options)
