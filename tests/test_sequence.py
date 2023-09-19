"""
Test cases for the `sequence` module.
"""
import unittest
from chew.string import alpha1, digit1
from chew.error import Error
from chew.generic import tag
from chew.sequence import *


class TestSequence(unittest.TestCase):
    def test_multiple(self):
        self.assertEqual(
            multiple([alpha1, digit1, alpha1])("abc123def"), ("", ("abc", "123", "def"))
        )

    def test_multiple_on_incomplete(self):
        with self.assertRaises(Error):
            multiple([digit1, alpha1, digit1])("123def")

    def test_delimited(self):
        self.assertEqual(
            delimited(tag("("), tag("abc"), tag(")"))("(abc)"),
            ("", "abc"),
        )

    def test_delimited_extra_content(self):
        self.assertEqual(
            delimited(tag("("), tag("abc"), tag(")"))("(abc)def"),
            ("def", "abc"),
        )

    def test_delimited_on_exhausted(self):
        with self.assertRaises(Error):
            delimited(tag("("), tag("abc"), tag(")"))("")

    def test_delimited_on_no_match(self):
        with self.assertRaises(Error):
            delimited(tag("("), tag("abc"), tag(")"))("123")

    def test_pair(self):
        self.assertEqual(pair(tag("abc"), tag("efg"))("abcefg"), ("", ("abc", "efg")))

    def test_pair_extra_content(self):
        self.assertEqual(
            pair(tag("abc"), tag("efg"))("abcefghij"), ("hij", ("abc", "efg"))
        )

    def test_pair_on_exhausted(self):
        with self.assertRaises(Error):
            pair(tag("abc"), tag("efg"))("")

    def test_pair_on_no_match(self):
        with self.assertRaises(Error):
            pair(tag("abc"), tag("efg"))("123")

    def test_preceded(self):
        self.assertEqual(preceded(tag("abc"), tag("efg"))("abcefg"), ("", "efg"))

    def test_preceded_extra_content(self):
        self.assertEqual(preceded(tag("abc"), tag("efg"))("abcefghij"), ("hij", "efg"))

    def test_preceded_on_exhausted(self):
        with self.assertRaises(Error):
            preceded(tag("abc"), tag("efg"))("")

    def test_preceded_on_no_match(self):
        with self.assertRaises(Error):
            preceded(tag("abc"), tag("efg"))("123")

    def test_separated_pair(self):
        self.assertEqual(
            separated_pair(tag("abc"), tag("|"), tag("efg"))("abc|efg"),
            ("", ("abc", "efg")),
        )

    def test_separated_pair_extra_content(self):
        self.assertEqual(
            separated_pair(tag("abc"), tag("|"), tag("efg"))("abc|efghij"),
            ("hij", ("abc", "efg")),
        )

    def test_separated_pair_on_exhausted(self):
        with self.assertRaises(Error):
            separated_pair(tag("abc"), tag("|"), tag("efg"))("")

    def test_separated_pair_on_no_match(self):
        with self.assertRaises(Error):
            separated_pair(tag("abc"), tag("|"), tag("efg"))("123")

    def test_terminated(self):
        self.assertEqual(terminated(tag("abc"), tag("efg"))("abcefg"), ("", "abc"))

    def test_terminated_extra_content(self):
        self.assertEqual(
            terminated(tag("abc"), tag("efg"))("abcefghij"), ("hij", "abc")
        )

    def test_terminated_on_exhausted(self):
        with self.assertRaises(Error):
            terminated(tag("abc"), tag("efg"))("")

    def test_terminated_on_no_match(self):
        with self.assertRaises(Error):
            terminated(tag("abc"), tag("efg"))("123")
