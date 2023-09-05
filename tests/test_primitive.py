"""
Sparse test cases for the `primitives` module.
"""

import unittest
from chew.primitive import *

TEST_STRING = "Hello World!\nI love Snails!\nThat is All."


class TestPrimitive(unittest.TestCase):
    def test_next_item_on_exhausted(self):
        self.assertEqual(next_item(""), None)

    def test_at_line(self):
        self.assertEqual(at_line(TEST_STRING, "Hello World!\nI love Snails!"), 1)

    def test_at_line_on_exhausted(self):
        self.assertEqual(at_line("", ""), 0)
