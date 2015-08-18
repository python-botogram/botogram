"""
    Tests for botogram/utils.py

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import botogram.utils


STRANGE_DOCSTRING = """ a


  b

"""


def test_format_docstr():
    # This docstring needs lots of cleanup...
    res = botogram.utils.format_docstr(STRANGE_DOCSTRING)
    assert res == "a\n\nb"

    # This instead should be left as it is
    ok = "a\nb"
    assert botogram.utils.format_docstr(ok) == ok
