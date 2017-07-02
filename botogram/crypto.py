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

import hmac


DIGEST = "md5"
DIGEST_LEN = 16


class TamperedMessageError(Exception):
    pass


def generate_secret_key(bot):
    """Generate the secret key of the bot"""
    mac = hmac.new(bot.api.token.encode("utf-8"), digestmod=DIGEST)
    mac.update(b"botogram" + bot.itself.username.encode("utf-8"))
    return mac.digest()


def get_hmac(bot, data):
    """Get the HMAC of a piece of data"""
    mac = hmac.new(generate_secret_key(bot), digestmod=DIGEST)
    mac.update(data)
    return mac.digest()


def sign_data(bot, data):
    """Return a signed version of the data, to prevent tampering with it"""
    return get_hmac(bot, data) + data


def verify_signature(bot, untrusted):
    """Check if the untrusted data is correctly signed, and return it"""
    if len(untrusted) < DIGEST_LEN:
        raise TamperedMessageError

    signature = untrusted[:DIGEST_LEN]
    data = untrusted[DIGEST_LEN:]

    if not hmac.compare_digest(get_hmac(bot, data), signature):
        raise TamperedMessageError

    return data


def compare(a, b):
    """Safely compare two values"""
    return hmac.compare_digest(a, b)
