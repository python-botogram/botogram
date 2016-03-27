"""
    botogram.api
    Wrapper for the Telegram Bot API

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import requests


class APIError(Exception):
    """Something went wrong with the API"""

    def __init__(self, response):
        self.error_code = response["error_code"]
        self.description = response["description"]

        msg = "Request failed with code %s. Response from Telegram: \"%s\"" % (
            self.error_code, self.description
        )

        super(APIError, self).__init__(msg)


class TelegramAPI:
    """Main interface to the Telegram API"""

    def __init__(self, api_key, endpoint=None):
        # Fill the default API endpoint
        if endpoint is None:
            endpoint = "https://api.telegram.org/"

        self._api_key = api_key
        self._endpoint = endpoint

    def call(self, method, params=None, files=None, expect=None):
        """Call a method of the API"""
        url = self._endpoint + "bot%s/%s" % (self._api_key, method)
        response = requests.get(url, params=params, files=files)
        content = response.json()

        if not content["ok"]:
            raise APIError(content)

        # If no special object is expected, return the decoded json.
        # Else, return the "pythonized" result
        if expect is None:
            return content
        else:
            wrapped = expect(content["result"])
            if hasattr(wrapped, "set_api"):
                wrapped.set_api(self)
            return wrapped

    def file_content(self, path):
        """Get the content of an user-submitted file"""
        url = self._endpoint + "file/bot%s/%s" % (self._api_key, path)
        response = requests.get(url)

        return response.content
