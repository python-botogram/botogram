"""
    Tests for botogram/objects/messages.py

    Copyright (c) 2016 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.objects.messages


def get_dummy_message(text):
    """Get a dummy message with a custom text"""
    return botogram.objects.messages.Message({
        "message_id": 1,
        "from": {"id": 123, "first_name": "Nobody"},
        "chat": {"id": -123, "type": "chat", "title": "Something"},
        "date": 1,
        "text": text,
    })


def parsed_to_list(parsed):
    """Convert a ParsedText to a list of entities"""
    return [(e.type, e.text) for e in parsed]


###################
##  Parsed text  ##
###################


def test_parsed_text_entity():
    msg = get_dummy_message("Hey, I'm an http://url.com")

    # Try to create an entity without an attached message
    entity = botogram.objects.messages.ParsedTextEntity({
        "type": "url",
        "offset": 12,
        "length": 14,
    })
    assert entity.type == "url"
    # Those attributes requires a Message instance
    with pytest.raises(RuntimeError):
        entity.url
    with pytest.raises(RuntimeError):
        entity.text

    # Now attach a message
    entity.set_message(msg)
    assert entity.url == "http://url.com"
    assert entity.text == "http://url.com"


def test_parsed_text_entity_url():
    # Basic entity
    entity = botogram.objects.messages.ParsedTextEntity({
        "type": "",
        "offset": 0,
        "length": 23,
    })

    # Url entity
    msg = get_dummy_message("https://www.example.com")
    entity.type = "url"
    entity.set_message(msg)
    assert entity.url == "https://www.example.com"

    # Mention entity
    msg = get_dummy_message("@a_botogram_users_group")
    entity.type = "mention"
    entity.set_message(msg)
    assert entity.url == "https://telegram.me/a_botogram_users_group"

    # Email entity
    msg = get_dummy_message("john.42.doe@example.com")
    entity.type = "email"
    entity.set_message(msg)
    assert entity.url == "mailto:john.42.doe@example.com"

    # Non-url type with a forced url
    msg = get_dummy_message("this is not an url, obv")
    entity.type = "plain"
    entity._url = "https://www.example.com"
    entity.set_message(msg)
    assert entity.url == "https://www.example.com"


def test_parsed_text():
    msg = get_dummy_message("This has an #hashtag!")
    parsed = botogram.objects.messages.ParsedText([
        {
            "type": "hashtag",
            "offset": 12,
            "length": 8,
        },
    ], message=msg)

    assert parsed_to_list(parsed) == [
        ("plain", "This has an "),
        ("hashtag", "#hashtag"),
        ("plain", "!"),
    ]
    assert parsed[0].text == "This has an "
    assert parsed[1].text == "#hashtag"
    assert parsed[2].text == "!"
    assert "plain" in parsed
    assert "hashtag" in parsed
    assert "url" not in parsed


def test_parsed_text_without_plain():
    # This needs an extra test because the "plain" types are not provided
    # directly by Telegram, but they're calculated dynamically by botogram
    msg = get_dummy_message("#hashtag")
    parsed = botogram.objects.messages.ParsedText([
        {
            "type": "hashtag",
            "offset": 0,
            "length": 8,
        },
    ], message=msg)

    assert parsed_to_list(parsed) == [
        ("hashtag", "#hashtag"),
    ]
    assert "plain" not in parsed


def test_parsed_text_filter():
    msg = get_dummy_message("I @mentioned #something!")
    parsed = botogram.objects.messages.ParsedText([
        {
            "type": "mention",
            "offset": 2,
            "length": 10,
        },
        {
            "type": "hashtag",
            "offset": 13,
            "length": 10,
        },
    ], message=msg)

    assert parsed_to_list(parsed) == [
        ("plain", "I "),
        ("mention", "@mentioned"),
        ("plain", " "),
        ("hashtag", "#something"),
        ("plain", "!"),
    ]
    assert parsed_to_list(parsed.filter("plain", "mention")) == [
        ("plain", "I "),
        ("mention", "@mentioned"),
        ("plain", " "),
        ("plain", "!"),
    ]
    assert parsed_to_list(parsed.filter("plain", exclude=True)) == [
        ("mention", "@mentioned"),
        ("hashtag", "#something"),
    ]
