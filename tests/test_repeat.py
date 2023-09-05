"""
Test cases for the `repeat` module.
"""
import unittest
from chew.error import ParseError
from chew.repeat import *

# TESTING IMPORTS
from chew.generic import tag
from chew.literal import int_literal


class TestRepeat(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count(tag("abc"), 2)("abcabc"), ("", ["abc", "abc"]))

    def test_count_fail_on_second(self):
        with self.assertRaises(ParseError):
            count(tag("abc"), 2)("abc123")

    def test_count_fail_on_both(self):
        with self.assertRaises(ParseError):
            count(tag("abc"), 2)("123123")

    def test_count_on_exhausted(self):
        with self.assertRaises(ParseError):
            count(tag("abc"), 2)("")

    def test_count_on_incomplete_match(self):
        self.assertEqual(count(tag("abc"), 2)("abcabcabc"), ("abc", ["abc", "abc"]))

    def test_length_count(self):
        self.assertEqual(
            length_count(int_literal, tag("abc"))("2abcabc"),
            ("", ["abc", "abc"]),
        )

    def test_length_count_on_sub_failure(self):
        with self.assertRaises(ParseError):
            length_count(int_literal, tag("abc"))("3defdefdef")

    def test_length_data(self):
        self.assertEqual(length_data(int_literal)("3abcefg"), ("efg", "abc"))

    def test_length_data_on_tiny(self):
        with self.assertRaises(ParseError):
            length_data(int_literal)("3a")

    def test_length_value(self):
        self.assertEqual(length_value(int_literal, tag("abc"))("3abcefg"), ("efg", "abc"))

    def test_length_value_on_sub_failure(self):
        with self.assertRaises(ParseError):
            length_value(int_literal, tag("abc"))("3defdefdef")

    def test_length_value_on_tiny(self):
        with self.assertRaises(ParseError):
            length_value(int_literal, tag("abc"))("3a")
