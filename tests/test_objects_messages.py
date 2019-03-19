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

import botogram.objects.messages
import botogram.objects.chats


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
    assert entity.type == "link"
    # Those attributes requires a Message instance
    with pytest.raises(RuntimeError):
        entity.url
    with pytest.raises(RuntimeError):
        entity.text

    # Now attach a message
    entity.set_message(msg)
    assert entity.url == "http://url.com"
    assert entity.text == "http://url.com"


def test_parsed_text_entity_type():
    # Basic entity
    entity = botogram.objects.messages.ParsedTextEntity({
        "type": "",
        "offset": 0,
        "length": 23,
    })

    #################################
    #  A type which doesn't mutate  #
    #################################

    msg = get_dummy_message("#aaaaaaaaaaaaaaaaaaaaaaa")
    entity.set_message(msg)

    # Getter
    entity._type = "hashtag"
    assert entity.type == "hashtag"

    # Setter
    entity.type = "hashtag"
    assert entity._type == "hashtag"

    #########################
    #  A type which mutate  #
    #########################

    msg = get_dummy_message("/aaaaaaaaaaaaaaaaaaaaaaa")
    entity.set_message(msg)

    # Getter
    entity._type = "bot_command"
    assert entity.type == "command"

    # Setter
    entity.type = "command"
    assert entity._type == "bot_command"

    #####################################
    #  A link (which mutates as "url")  #
    #####################################

    msg = get_dummy_message("https://www.example.com")
    entity.set_message(msg)

    # Getter
    entity._type = "url"
    assert entity.type == "link"

    # Setter without URL explicitly defined
    entity.type = "link"
    assert entity._type == "url"

    # Setter with URL explicitly defined
    entity._url = "https://www.example.com"
    entity.type = "link"
    assert entity._type == "url"

    ###########################################
    #  A link (which mutates as "text_link")  #
    ###########################################

    msg = get_dummy_message("This is a labelled link")
    entity._url = "https://www.example.com"
    entity.set_message(msg)

    # Getter
    entity._type = "text_link"
    assert entity.type == "link"

    # Setter
    entity.type = "link"
    assert entity._type == "text_link"

    ############################################
    #  A mention (which mutates as "mention")  #
    ############################################

    msg = get_dummy_message("@test_image")
    entity.set_message(msg)

    # Getter
    entity._type = "mention"
    assert entity.type == "mention"

    # Setter
    entity.type = "mention"
    assert entity._type == "mention"

    #################################################
    #  A mention (which mutates as "text_mention")  #
    #################################################

    msg = get_dummy_message("@test_image")
    entity.user = botogram.objects.chats.User({"id": 1, "first_name": "Test"})
    entity.set_message(msg)

    # Getter
    entity._type = "text_mention"
    assert entity.type == "mention"

    # Setter
    entity.type = "mention"
    assert entity._type == "text_mention"

    entity.user = None


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

    # Mention entity with @usernames
    msg = get_dummy_message("@a_botogram_users_group")
    entity.type = "mention"
    entity.set_message(msg)
    assert entity.url == "https://telegram.me/a_botogram_users_group"

    # Text mention entities without usernames
    msg = get_dummy_message("A botogram users group!")
    entity.user = botogram.objects.chats.User({"id": 1, "first_name": "Test"})
    entity.type = "mention"
    entity.set_message(msg)
    assert entity.url is None

    # Text mention entities with usernames
    entity.user.username = "test_username"
    assert entity.url == "https://telegram.me/test_username"

    entity.user = None

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
    entity._url = None

    # Url entity without a scheme
    msg = get_dummy_message("www.example.com/abcdefg")
    entity.type = "url"
    entity.set_message(msg)
    assert entity.url == "http://www.example.com/abcdefg"


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
