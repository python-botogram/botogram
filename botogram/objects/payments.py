"""
    botogram.objects.payments
    Representation of payments-related upstream API objects

    Copyright (c) 2017 Marco Aceti <dev@marcoaceti.it>
    Released under the MIT license
"""

from .mixins import ShippingQueryMixin, PreCheckoutQueryMixin
from .base import BaseObject
from .chats import User


class Invoice(BaseObject):
    required = {
        "title": str,
        "description": str,
        "start_parameter": str,
        "currency": str,
        "total_amount": int,
    }


class LabeledPrice(BaseObject):
    required = {
        "label": str,
        "amount": int,
    }


class ShippingOption(BaseObject):
    required = {
        "id": str,
        "title": str,
        "prices": LabeledPrice,
    }


class ShippingAddress(BaseObject):
    required = {
        "country_code": str,
        "state": str,
        "city": str,
        "street_line1": str,
        "street_line2": str,
        "post_code": str,
    }


class OrderInfo(BaseObject):
    optional = {
        "name": str,
        "phone_number": str,
        "email": str,
        "shipping_address": ShippingAddress,
    }


class SuccessfulPayment(BaseObject):
    required = {
        "currency": str,
        "total_amount": int,
        "invoice_payload": str,
        "telegram_payment_charge_id": str,
        "provider_payment_charge_id": str,
    }
    optional = {
        "shipping_option_id": str,
        "order_info": OrderInfo,
    }


class ShippingQuery(BaseObject, ShippingQueryMixin):
    required = {
        "id": str,
        "from": User,
        "invoice_payload": str,
        "shipping_address": ShippingAddress,
    }
    replace_keys = {
        "from": "sender",
    }

    def __init__(self, data, api=None):
        super().__init__(data, api)


class PreCheckoutQuery(BaseObject, PreCheckoutQueryMixin):
    required = {
        "id": str,
        "from": User,
        "currency": str,
        "total_amount": int,
        "invoice_payload": str,
    }
    optional = {
        "shipping_option_id": str,
        "order_info": OrderInfo,
    }
    replace_keys = {
        "from": "sender",
    }

    def __init__(self, data, api=None):
        super().__init__(data, api)
