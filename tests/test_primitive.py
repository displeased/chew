"""
Sparse test cases for the `primitives` module.
"""

import unittest
from chew.primitive import *

TEST_STRING = "Hello World!\nI love Snails!\nThat is All."
ONE_LINES = "\nI love Snails!\nThat is All."
TWO_LINES = "\nThat is All."
THREE_LINES = ""


class TestPrimitive(unittest.TestCase):
    def test_take_on_exhausted(self):
        self.assertEqual(take("", 1), None)

    def test_next_item_on_exhausted(self):
        self.assertEqual(next_item(""), None)

    def test_at_line(self):
        self.assertEqual(at_line(TEST_STRING, ONE_LINES), 0)

    def test_at_line_two_lines(self):
        self.assertEqual(at_line(TEST_STRING, TWO_LINES), 1)

    def test_at_line_three_lines(self):
        self.assertEqual(at_line(TEST_STRING, THREE_LINES), 2)

    def test_at_line_on_exhausted(self):
        self.assertEqual(at_line("", ""), 0)
