"""
Test cases for the `repeat` module.
"""
import unittest
from typing import TypeVar
from tests import assert_error
from chew.error import Error, ErrorKind
from chew.repeat import *

# TESTING IMPORTS
from chew.string import alpha0
from chew.generic import tag
from chew.literal import int_literal

T = TypeVar("T")


class TestRepeat(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count(tag("abc"), 2)("abcabc"), ("", ["abc", "abc"]))

    def test_count_fail_on_second(self):
        with assert_error(self, Error("123", ErrorKind.TAG)):
            count(tag("abc"), 2)("abc123")

    def test_count_fail_on_both(self):
        with assert_error(self, Error("123123", ErrorKind.TAG)):
            count(tag("abc"), 2)("123123")

    def test_count_on_exhausted(self):
        with assert_error(self, Error("", ErrorKind.TAG)):
            count(tag("abc"), 2)("")

    def test_count_on_incomplete_match(self):
        self.assertEqual(count(tag("abc"), 2)("abcabcabc"), ("abc", ["abc", "abc"]))

    def test_fill(self):
        buffer = ["", ""]

        self.assertEqual(fill(tag("abc"), buffer)("abcabc"), ("", None))
        self.assertEqual(buffer, ["abc", "abc"])

    def test_fill_partial_fail(self):
        buffer = ["", ""]

        with assert_error(self, Error("123", ErrorKind.TAG)):
            fill(tag("abc"), buffer)("abc123")

    def test_fill_no_match(self):
        buffer = ["", ""]

        with assert_error(self, Error("123123", ErrorKind.TAG)):
            fill(tag("abc"), buffer)("123123")

    def test_fill_on_exhausted(self):
        buffer = ["", ""]

        with assert_error(self, Error("", ErrorKind.TAG)):
            fill(tag("abc"), buffer)("")

    def test_fill_partial_match(self):
        buffer = ["", ""]

        self.assertEqual(fill(tag("abc"), buffer)("abcabcabc"), ("abc", None))
        self.assertEqual(buffer, ["abc", "abc"])

    def test_fold_many0(self):
        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("abcabc"), ("", ["abc", "abc"]))

    def test_fold_many0_partial(self):
        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("abc123"), ("123", ["abc"]))

    def test_fold_many0_no_match(self):
        parser = fold_many0(tag("abc"), list, list_append)
        self.assertEqual(parser("123123"), ("123123", []))

    def test_fold_many0_on_exhausted(self):
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
        parser = fold_many1(tag("abc"), list, list_append)
        self.assertEqual(parser("abcabc"), ("", ["abc", "abc"]))

    def test_fold_many1_partial(self):
        parser = fold_many1(tag("abc"), list, list_append)
        self.assertEqual(parser("abc123"), ("123", ["abc"]))

    def test_fold_many1_no_match(self):
        parser = fold_many1(tag("abc"), list, list_append)
        with assert_error(self, Error("123123", ErrorKind.MANY1)):
            parser("123123")

    def test_fold_many1_on_exhausted(self):
        parser = fold_many1(tag("abc"), list, list_append)
        with assert_error(self, Error("", ErrorKind.MANY1)):
            parser("")

    def test_fold_many_bounded(self):
        parser = fold_many_bounded(1, 2, tag("abc"), list, list_append)
        self.assertEqual(parser("abcabc"), ("", ["abc", "abc"]))

    def test_fold_many_bounded_one_match(self):
        parser = fold_many_bounded(1, 2, tag("abc"), list, list_append)
        self.assertEqual(parser("abc123"), ("123", ["abc"]))

    def test_fold_many_bounded_no_match(self):
        parser = fold_many_bounded(1, 2, tag("abc"), list, list_append)
        with assert_error(self, Error("123123", ErrorKind.FOLD_MANY_BOUNDED)):
            parser("123123")

    def test_fold_many_bounded_on_exhausted(self):
        parser = fold_many_bounded(0, 2, tag("abc"), list, list_append)
        self.assertEqual(parser(""), ("", []))

    def test_fold_many_bounded_on_incomplete(self):
        parser = fold_many_bounded(0, 2, tag("abc"), list, list_append)
        self.assertEqual(parser("abcabcabc"), ("abc", ["abc", "abc"]))

    def test_length_count_on_sub_failure(self):
        with assert_error(self, Error("defdefdef", ErrorKind.TAG)):
            length_count(int_literal, tag("abc"))("3defdefdef")

    def test_length_data(self):
        self.assertEqual(length_data(int_literal)("3abcefg"), ("efg", "abc"))

    def test_length_data_on_tiny(self):
        with assert_error(self, Error("a", ErrorKind.EOF)):
            length_data(int_literal)("3a")

    def test_length_value(self):
        self.assertEqual(
            length_value(int_literal, tag("abc"))("3abcefg"), ("efg", "abc")
        )

    def test_length_value_on_sub_failure(self):
        with assert_error(self, Error("def", ErrorKind.TAG)):
            length_value(int_literal, tag("abc"))("3defdef")

    def test_length_value_on_tiny(self):
        with assert_error(self, Error("a", ErrorKind.EOF)):
            length_value(int_literal, tag("abc"))("3a")

    def test_many0(self):
        self.assertEqual(many0(tag("abc"))("abcabc"), ("", ["abc", "abc"]))

    def test_many0_on_partial(self):
        self.assertEqual(many0(tag("abc"))("abc123"), ("123", ["abc"]))

    def test_many0_on_no_matches(self):
        self.assertEqual(many0(tag("abc"))("123123"), ("123123", []))

    def test_many0_on_exhausted(self):
        self.assertEqual(many0(tag("abc"))(""), ("", []))

    def test_many0_on_infinite(self):
        self.assertEqual(many0(alpha0)("abc"), ("", ["abc"]))

    def test_many0_count(self):
        self.assertEqual(many0_count(tag("abc"))("abcabc"), ("", 2))

    def test_many0_count_on_partial(self):
        self.assertEqual(many0_count(tag("abc"))("abc123"), ("123", 1))

    def test_many0_count_on_no_matches(self):
        self.assertEqual(many0_count(tag("abc"))("123123"), ("123123", 0))

    def test_many0_count_on_exhausted(self):
        self.assertEqual(many0_count(tag("abc"))(""), ("", 0))

    def test_many1(self):
        self.assertEqual(many1(tag("abc"))("abcabc"), ("", ["abc", "abc"]))

    def test_many1_on_partial(self):
        self.assertEqual(many1(tag("abc"))("abc123"), ("123", ["abc"]))

    def test_many1_on_no_matches(self):
        with assert_error(self, Error("123123", ErrorKind.TAG)):
            many1(tag("abc"))("123123")

    def test_many1_on_exhausted(self):
        with assert_error(self, Error("", ErrorKind.TAG)):
            many1(tag("abc"))("")

    def test_many1_on_infinite(self):
        self.assertEqual(many1(alpha0)("abc"), ("", ["abc"]))


def list_append(acc: list[T], item: T) -> list[T]:
    acc.append(item)
    return acc
