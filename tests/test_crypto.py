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

import pytest

from botogram.crypto import generate_secret_key, get_hmac, sign_data
from botogram.crypto import TamperedMessageError, verify_signature


def test_generate_secret_key(bot):
    # Check if the generated key for the test bot is correct
    key = generate_secret_key(bot)
    assert key == b'\\\x93aA\xe8\x8d\x9aL\x8c\xfd\x81,D\xeaj\xd0'


def test_hmac(bot):
    expect = b'q\x06\x9c\xc1\xfa\xd1n\xe8\xef\x17\xf6\xd7Z\xb0G\x7f'
    assert get_hmac(bot, b'test data') == expect

    signed = sign_data(bot, b'test string')
    assert verify_signature(bot, signed) == b'test string'

    signed += b'a'
    with pytest.raises(TamperedMessageError):
        verify_signature(bot, signed)

    with pytest.raises(TamperedMessageError):
        verify_signature(bot, b'a')
