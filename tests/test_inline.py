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
import json
import botogram
from botogram.components import Component
from botogram.objects.updates import Update
from botogram.hooks import InlineHook
from botogram.runner.jobs import _inline_assign_worker


def call_overwrite(*args):
    for arg in args:
        if type(arg) is dict:
            if "results" in arg:
                arg["results"] = json.loads(arg["results"])
    return args


def update_inline(id_update, offset='', query=''):
    return Update({
        'update_id': id_update,
        'inline_query': {
            'id': '123',
            'from': {
                'id': 321,
                'is_bot': False,
                'first_name': 'test_name'
            },
            'query': query,
            'offset': offset
        }
    })


def expected_result_inline(old_offset=0):
    r = []
    for i in range(old_offset, old_offset+10):
        r.append({"id": i,
                  "title": "test title",
                  "input_message_content": {
                      "message_text": "test message",
                      "disable_web_page_preview": False},
                  "type": "article"})

    return {'inline_query_id': '123',
                       'cache_time': 0,
                       'is_personal': True,
                       'results': r,
                       'next_offset': old_offset+10}


def inline_default(bot):
    def inline_test(inline):
        for i in range(50):
            yield inline.article("test title",
                                 botogram.InlineInputMessage("test message"))
    inline_func = bot.inline()(inline_test)
    return {'inline': [InlineHook(inline_func,
                                  Component(),
                                  {'cache': 0, 'private': True,
                                   'paginate': 10, 'timer': 60})]}


def test_worker_assignment():
    update_1 = update_inline(1)
    assert _inline_assign_worker(update_1, 5) == 4
    update_2 = update_inline(2, offset='10',
                             query='Test query with some unicode 🅱️🤯🥶')
    assert _inline_assign_worker(update_2, 3) == 2


def test_inline_hook(bot, mock_req):
    chains = inline_default(bot)
    update = update_inline(1)
    bot.api.call = call_overwrite
    for hook in chains["inline"]:
        result = hook.call(bot, update)
    assert result[0] == 'answerInlineQuery'
    assert result[1] == expected_result_inline(0)


def test_paginate(bot, mock_req):
    chains = inline_default(bot)
    bot.api.call = call_overwrite

    for i in range(0, 5):
        update = update_inline(i, str(i*10))
        for hook in chains["inline"]:
            result = hook.call(bot, update)
            assert result[0] == 'answerInlineQuery'
            assert result[1] == expected_result_inline(i*10)

    result = None
    update = update_inline(5, str(5*10))
    for hook in chains['inline']:
        result = hook.call(bot, update)
    assert result is None
