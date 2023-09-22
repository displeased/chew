"""
Test cases for the `repeat` module.
"""
import unittest
from chew.error import Error, ErrorKind
from chew.repeat import *

# TESTING IMPORTS
from chew.generic import tag
from chew.literal import int_literal


class TestRepeat(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count(tag("abc"), 2)("abcabc"), ("", ["abc", "abc"]))

    def test_count_fail_on_second(self):
        with self.assertRaises(Error) as context:
            count(tag("abc"), 2)("abc123")

        self.assertEqual(context.exception, Error("123", ErrorKind.TAG))

    def test_count_fail_on_both(self):
        with self.assertRaises(Error) as context:
            count(tag("abc"), 2)("123123")

        self.assertEqual(context.exception, Error("123123", ErrorKind.TAG))

    def test_count_on_exhausted(self):
        with self.assertRaises(Error) as context:
            count(tag("abc"), 2)("")

        self.assertEqual(context.exception, Error("", ErrorKind.TAG))

    def test_count_on_incomplete_match(self):
        self.assertEqual(count(tag("abc"), 2)("abcabcabc"), ("abc", ["abc", "abc"]))

    def test_length_count(self):
        self.assertEqual(
            length_count(int_literal, tag("abc"))("2abcabc"),
            ("", ["abc", "abc"]),
        )

    def test_length_count_on_sub_failure(self):
        with self.assertRaises(Error) as context:
            length_count(int_literal, tag("abc"))("3defdefdef")

        self.assertEqual(context.exception, Error("defdefdef", ErrorKind.TAG))

    def test_length_data(self):
        self.assertEqual(length_data(int_literal)("3abcefg"), ("efg", "abc"))

    def test_length_data_on_tiny(self):
        with self.assertRaises(Error) as context:
            length_data(int_literal)("3a")

        self.assertEqual(context.exception, Error("a", ErrorKind.EOF))

    def test_length_value(self):
        self.assertEqual(
            length_value(int_literal, tag("abc"))("3abcefg"), ("efg", "abc")
        )

    def test_length_value_on_sub_failure(self):
        with self.assertRaises(Error) as context:
            length_value(int_literal, tag("abc"))("3defdef")

        self.assertEqual(context.exception, Error("def", ErrorKind.TAG))

    def test_length_value_on_tiny(self):
        with self.assertRaises(Error) as context:
            length_value(int_literal, tag("abc"))("3a")

        self.assertEqual(context.exception, Error("a", ErrorKind.EOF))
