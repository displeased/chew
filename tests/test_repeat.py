"""
Test cases for the `repeat` module.
"""
import unittest
from chew.error import Error, ErrorKind
from chew.repeat import *

# TESTING IMPORTS
from chew.string import alpha0
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

    def test_fill(self):
        buffer = ["", ""]

        self.assertEqual(fill(tag("abc"), buffer)("abcabc"), ("", None))
        self.assertEqual(buffer, ["abc", "abc"])

    def test_fill_partial_fail(self):
        buffer = ["", ""]

        with self.assertRaises(Error) as context:
            fill(tag("abc"), buffer)("abc123")

        self.assertEqual(context.exception, Error("123", ErrorKind.TAG))

    def test_fill_no_match(self):
        buffer = ["", ""]

        with self.assertRaises(Error) as context:
            fill(tag("abc"), buffer)("123123")
        self.assertEqual(context.exception, Error("123123", ErrorKind.TAG))

    def test_fill_on_exhausted(self):
        buffer = ["", ""]

        with self.assertRaises(Error) as context:
            fill(tag("abc"), buffer)("")
        self.assertEqual(context.exception, Error("", ErrorKind.TAG))

    def test_fill_partial_match(self):
        buffer = ["", ""]

        self.assertEqual(fill(tag("abc"), buffer)("abcabcabc"), ("abc", None))
        self.assertEqual(buffer, ["abc", "abc"])

    def test_fold_many0(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("abcabc"), ("", ["abc", "abc"]))

    def test_fold_many0_partial(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("abc123"), ("123", ["abc"]))

    def test_fold_many0_no_match(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("123123"), ("123123", []))

    def test_fold_many0_on_exhausted(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser(""), ("", []))

    def test_fold_many0_on_empty_allowed(self):
        parser = fold_many0(alpha0, list, lambda acc, item: acc)
        self.assertEqual(parser(""), ("", []))

    def test_length_count(self):
        self.assertEqual(
            length_count(int_literal, tag("abc"))("2abcabc"),
            ("", ["abc", "abc"]),
        )

    def test_fold_many1(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many1(tag("abc"), list, list_append)
        self.assertEqual(parser("abcabc"), ("", ["abc", "abc"]))

    def test_fold_many1_partial(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many1(tag("abc"), list, list_append)
        self.assertEqual(parser("abc123"), ("123", ["abc"]))

    def test_fold_many1_no_match(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many1(tag("abc"), list, list_append)
        with self.assertRaises(Error) as context:
            parser("123123")
        self.assertEqual(context.exception, Error("123123", ErrorKind.MANY1))

    def test_fold_many1_on_exhausted(self):
        def list_append(acc, item):
            acc.append(item)
            return acc

        parser = fold_many1(tag("abc"), list, list_append)
        with self.assertRaises(Error) as context:
            parser("")
        self.assertEqual(context.exception, Error("", ErrorKind.MANY1))

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
