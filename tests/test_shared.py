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

import pickle

import botogram.shared
import botogram.hooks


def test_shared_memory_creation():
    shared = botogram.shared.SharedMemory()

    comp1 = shared.of("bot1", "comp1")
    comp2 = shared.of("bot1", "comp2")
    comp1b = shared.of("bot1", "comp1")
    comp1sub = shared.of("bot1", "comp1", "sub")

    comp1["test"] = "test"

    assert "test" in comp1
    assert "test" in comp1b
    assert not comp2  # empty
    assert comp1["test"] == comp1b["test"]
    assert not comp1sub  # empty

    # memory3sub has more than two parts in a name, so special shared memory
    # methods should not have been applied
    assert not hasattr(comp1sub, "lock")


def test_shared_memory_preparers():
    shared = botogram.shared.SharedMemory()

    def init1(shared):
        if "a" in shared:
            shared["a"] = 1
        else:
            shared["a"] = 0

    def init2(shared):
        shared["b"] = 1

    comp = botogram.Component()
    init1_hook = botogram.hooks.MemoryPreparerHook(init1, comp)
    init2_hook = botogram.hooks.MemoryPreparerHook(init2, comp)

    shared.register_preparers_list("comp1", [init1_hook, init2_hook])
    shared.register_preparers_list("comp2", [init1_hook])

    memory1 = shared.of("bot1", "comp1")
    memory2 = shared.of("bot1", "comp2")
    memory3 = shared.of("bot2", "comp1")
    memory3sub = shared.of("bot2", "comp1", "sub")

    assert memory1["a"] == 0
    assert memory1["b"] == 1
    assert memory2["a"] == 0
    assert "b" not in memory2
    # memory3["a"] should be 1 if the initializer was called multiple times
    assert memory3["a"] == 0

    # memory3sub has more than two parts in a name, so no preparer should have
    # been applied
    assert "a" not in memory3sub

    # memory1b["a"] should be 1 if the initializer was called multiple times
    memory1b = shared.of("bot1", "comp1")
    assert memory1b["a"] == 0


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
