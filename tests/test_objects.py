"""
    Tests for botogram/objects/__init__.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pytest

import botogram.objects


def test_photo_object():
    # The Photo object is custom-made, so it's better to ensure all it's
    # working as expected
    data = [
        {"file_id": "aaaaaa", "width": 10, "height": 10, "file_size": 48},
        {"file_id": "aaaaaa", "width": 20, "height": 20, "file_size": 148},
        {"file_id": "aaaaaa", "width": 30, "height": 30, "file_size": 248},
    ]

    # Let's create a valid Photo object
    photo = botogram.objects.Photo(data)
    assert len(photo.sizes) == len(data)
    assert photo.sizes[0].file_id == data[0]["file_id"]
    assert photo.smallest.file_id == data[0]["file_id"]
    assert photo.biggest.file_id == data[-1]["file_id"]
    assert photo.biggest.file_id == photo.file_id
    assert photo.serialize() == data

    # Test if set_api is working
    photo2 = botogram.objects.Photo(data, "testapi")
    assert photo2._api == "testapi"
    assert photo2.sizes[0]._api == "testapi"
    photo2.set_api("anotherapi")
    assert photo2._api == "anotherapi"
    assert photo2.sizes[0]._api == "anotherapi"

    # Empty PhotoSize not supported, sorry
    with pytest.raises(ValueError):
        botogram.objects.Photo([])

    # The data provided must be a list
    with pytest.raises(ValueError):
        botogram.objects.Photo("I'm not a list (doh)")

    # And the items inside a list must be PhotoSize
    with pytest.raises(ValueError):
        botogram.objects.Photo([{"This": "isn't", "a": "PhotoSize"}])
