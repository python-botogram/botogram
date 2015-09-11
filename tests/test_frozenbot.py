"""
    Tests for botogram/frozenbot.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import pickle


def test_pickle_frozenbot(frozenbot):
    # This will pickle and unpickle the frozen bot
    pickled = pickle.loads(pickle.dumps(frozenbot))
    assert frozenbot == pickled
