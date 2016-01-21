"""
    Tests for botogram/syntaxes.py

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.syntaxes


def test_is_markdown():
    assert not botogram.syntaxes.is_markdown("not markdown, sorry!")
    assert not botogram.syntaxes.is_markdown("*a [wonderfully](broken syntax`")

    for delimiter in "*", "_", "`", "```":
        assert botogram.syntaxes.is_markdown(delimiter+"a"+delimiter)

    assert botogram.syntaxes.is_markdown("[a](b)")


def test_is_html():
    assert not botogram.syntaxes.is_html("not HTML, sorry!")
    assert not botogram.syntaxes.is_html("<a some </really> <b>roken html</i>")

    for tag in "b", "strong", "i", "em", "pre", "code":
        assert botogram.syntaxes.is_html("<"+tag+">a</"+tag+">")

    assert not botogram.syntaxes.is_html("<a>a</a>")
    assert not botogram.syntaxes.is_html("<a test=\"b\">a</a>")
    assert botogram.syntaxes.is_html("<a href=\"b\">a</a>")


def test_guess_syntax():
    # Provided syntax name
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
