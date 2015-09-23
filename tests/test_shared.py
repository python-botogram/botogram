"""
    Tests for botogram/shared.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pickle

import botogram.shared


def test_shared_memory_creation():
    shared = botogram.shared.SharedMemory()

    comp1 = shared.of("bot1", "comp1")
    comp2 = shared.of("bot1", "comp2")
    comp1b = shared.of("bot1", "comp1")

    comp1["test"] = "test"

    assert "test" in comp1
    assert "test" in comp1b
    assert not comp2  # empty
    assert comp1["test"] == comp1b["test"]


def test_shared_memory_pickleable():
    shared = botogram.shared.SharedMemory()
    shared.of("bot1", "comp1")["test"] = "test"

    pickled = pickle.loads(pickle.dumps(shared))

    original = shared.of("bot1", "comp1")["test"]
    assert original == pickled.of("bot1", "comp1")["test"]


def test_switch_driver():
    shared = botogram.shared.SharedMemory()

    # Initialize the memory with some dummy data
    shared.of("bot1", "test1")["a"] = "b"
    shared.of("bot1", "test2")["b"] = "c"

    # Create a new driver
    driver = botogram.shared.LocalDriver()
    shared.switch_driver(driver)

    assert shared.driver == driver
    assert shared.of("bot1", "test1")["a"] == "b"
    assert shared.of("bot1", "test2")["b"] == "c"
