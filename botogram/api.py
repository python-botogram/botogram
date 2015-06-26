"""
    botogram.api
    Wrapper for the Telegram Bot API

    Copyright (c) 2015 Pietro Albini
    Released under the MIT license
"""

import requests

from . import objects


class APIError(Exception):
    """Something went wrong with the API"""
    pass


class TelegramAPI:
    """Main interface to the Telegram API"""

    def __init__(self, api_key, endpoint=None):
        # Fill the default API endpoint
        if endpoint is None:
            endpoint = "https://api.telegram.org/bot{api_key}/{method}"

        self._api_key = api_key
        self._endpoint = endpoint

    def call(self, method, params=None, expect=None):
        """Call a method of the API"""
        url = self._endpoint.format(api_key=self._api_key, method=method)
        response = requests.get(url, params=params)
        content = response.json()

        if not content["ok"]:
            raise APIError("Request returned an error response: %s"
                           % response.text)

        # If no special object is expected, return the decoded json.
        # Else, return the "pythonized" result
        if expect is None:
            return content
        else:
            wrapped = expect(content["result"])
            if hasattr(wrapped, "set_api"):
                wrapped.set_api(self)
            return wrapped
