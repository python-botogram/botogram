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

from botogram.components import Component
from botogram.objects.updates import Update
from botogram.hooks import InlineHook
from botogram.runner.jobs import _inline_assign_worker


def inline_default(bot):
    def inline_test(inline):
        for i in range(50):
            yield inline.article("test title",
                                 "test message")
    inline_func = bot.inline()(inline_test)
    return {'inline': [InlineHook(inline_func,
                                  Component(),
                                  {'cache': 0, 'private': True,
                                   'paginate': 10, 'timer': 60})]}


def test_worker_assignment():
    update_1 = Update({
        'update_id': 1,
        'inline_query': {
            'id': '123456789012345',
            'from': {
                'id': '12345678',
                'is_bot': False,
                'first_name': 'test_name',
            },
            'query': '',
            'offset': '',
        }
    })
    assert _inline_assign_worker(update_1, 5) == 1

    update_2 = Update({
        'update_id': 2,
        'inline_query': {
            'id': '0987654321012345',
            'from': {
                'id': '87654321',
                'is_bot': False,
                'first_name': 'test_name',
            },
            'query': 'Test query with some unicode 🅱️🤯🥶',
            'offset': '10',
        }
    })
    assert _inline_assign_worker(update_2, 3) == 2


def test_inline_hook(bot, mock_req):
    chains = inline_default(bot)
    update = Update({
        'update_id': 1,
        'inline_query': {
            'id': '123',
            'from': {
                'id': 321,
                'is_bot': False,
                'first_name': 'test_name'
            },
            'query': '',
            'offset': ''
        }
    })
    mock_req({
        'answerInlineQuery': {'ok': True, 'result': True}
    })
    bot._update_processors['inline_query'](bot, chains, update)


def test_paginate(bot, mock_req):
    return "¿?"
    chains = inline_default(bot)
    update = Update({
        'update_id': 1,
        'inline_query': {
            'id': '123',
            'from': {
                'id': 321,
                'is_bot': False,
                'first_name': 'test_name'
            },
            'query': 'myquery',
            'offset': ''
        }
    })
    mock_req({
        'answerInlineQuery': {
            'ok': True,
            'result': True
        }
    })
    bot._update_processors['inline_query'](bot, chains, update)
    assert False
