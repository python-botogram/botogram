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

import botogram.syntaxes


def test_is_markdown():
    assert not botogram.syntaxes.is_markdown("not markdown, sorry!")
    assert not botogram.syntaxes.is_markdown("*a [wonderfully](broken syntax`")

    for delimiter in "*", "_", "`", "```":
        assert botogram.syntaxes.is_markdown(delimiter+"a"+delimiter)
        assert botogram.syntaxes.is_markdown("!"+delimiter+"a"+delimiter+"!")
        assert botogram.syntaxes.is_markdown("a\n"+delimiter+"a"+delimiter)
        assert botogram.syntaxes.is_markdown("a"+delimiter+"a\na"+delimiter)

    assert botogram.syntaxes.is_markdown("[a](b)")
    assert botogram.syntaxes.is_markdown("![a](b)!")
    assert botogram.syntaxes.is_markdown("a\n[a](b)")
    assert botogram.syntaxes.is_markdown("a[a\na](b)")
    assert botogram.syntaxes.is_markdown("a[a](b\nb)")

    assert not botogram.syntaxes.is_markdown("hey@this_is_awesome.com")
    assert not botogram.syntaxes.is_markdown("https://www.this_is_awesome.com")


def test_is_html():
    assert not botogram.syntaxes.is_html("not HTML, sorry!")
    assert not botogram.syntaxes.is_html("<a some </really> <b>roken html</i>")

    for tag in "b", "strong", "i", "em", "pre", "code":
        assert botogram.syntaxes.is_html("<"+tag+">a</"+tag+">")
        assert botogram.syntaxes.is_html("!<"+tag+">a</"+tag+">!")
        assert botogram.syntaxes.is_html("a\n<"+tag+">a</"+tag+">")
        assert botogram.syntaxes.is_html("a<"+tag+">a\na</"+tag+">")

    assert not botogram.syntaxes.is_html("<a>a</a>")
    assert not botogram.syntaxes.is_html("<a test=\"b\">a</a>")
    assert botogram.syntaxes.is_html("<a href=\"b\">a</a>")
    assert botogram.syntaxes.is_html("!<a href=\"b\">a</a>!")
    assert botogram.syntaxes.is_html("a\n<a href=\"b\">a</a>")
    assert botogram.syntaxes.is_html("a<a href=\"b\">a\na</a>")
    assert botogram.syntaxes.is_html("a<a href=\"b\nb\">a</a>")


def test_guess_syntax():
    # Provided syntax name
    for name in ("plain",):
        assert botogram.syntaxes.guess_syntax("", name) is None

    for name in ("md", "markdown", "Markdown"):
        assert botogram.syntaxes.guess_syntax("", name) == "Markdown"

    for name in ("html", "HTML"):
        assert botogram.syntaxes.guess_syntax("", name) == "HTML"

    with pytest.raises(ValueError):
        botogram.syntaxes.guess_syntax("", "invalid")

    # Let's guess it
    assert botogram.syntaxes.guess_syntax("no syntax, sorry!", None) is None
    assert botogram.syntaxes.guess_syntax("*markdown*", None) == "Markdown"
    assert botogram.syntaxes.guess_syntax("<b>html</b>", None) == "HTML"
