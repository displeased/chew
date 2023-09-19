"""
Test cases for the `generic` module.
"""
import unittest
import string as stdstring
from chew.error import Error
from chew.generic import *


class TestGeneric(unittest.TestCase):
    def test_tag(self):
        """Tag matches successfully."""
        self.assertEqual(tag("Hello")("Hello, World!"), (", World!", "Hello"))

    def test_tag_fail(self):
        """Tag with no match."""
        with self.assertRaises(Error):
            tag("Hello")("Something")

    def test_take(self):
        self.assertEqual(take(6)("1234567"), ("7", "123456"))

    def test_take_overtake(self):
        with self.assertRaises(Error):
            take(6)("short")

    def test_take_on_exhausted(self):
        with self.assertRaises(Error):
            take(6)("")

    def test_take_till(self):
        self.assertEqual(take_till(lambda c: c == ":")("latin:123"), (":123", "latin"))

    def test_take_till_empty_match(self):
        self.assertEqual(
            take_till(lambda c: c == ":")(":empty matched"),
            (":empty matched", ""),
        )

    def test_take_till_no_match(self):
        self.assertEqual(take_till(lambda c: c == ":")("12345"), ("", "12345"))

    def test_take_till_on_exhausted(self):
        self.assertEqual(take_till(lambda c: c == ":")(""), ("", ""))

    def test_take_while(self):
        self.assertEqual(
            take_while(lambda c: c in stdstring.ascii_letters)("latin123"),
            ("123", "latin"),
        )

    def test_take_while_no_match(self):
        self.assertEqual(
            take_while(lambda c: c in stdstring.ascii_letters)("12345"), ("12345", "")
        )

    def test_take_while_all_match(self):
        self.assertEqual(
            take_while(lambda c: c in stdstring.ascii_letters)("latin"), ("", "latin")
        )

    def test_take_while_on_exhausted(self):
        self.assertEqual(
            take_while(lambda c: c in stdstring.ascii_letters)(""), ("", "")
        )

    def test_is_a(self):
        self.assertEqual(
            is_a(stdstring.hexdigits)("123 and voila"), (" and voila", "123")
        )

    def test_is_a_longer(self):
        self.assertEqual(
            is_a(stdstring.hexdigits)("DEADBEEF and others"),
            (" and others", "DEADBEEF"),
        )

    def test_is_a_conjoined(self):
        self.assertEqual(
            is_a("ABCDEFGHIJKLMNOPQRSTUVWXYZ")("BADBABEsomething"),
            ("something", "BADBABE"),
        )

    def test_is_a_all_match(self):
        self.assertEqual(is_a(stdstring.hexdigits)("D15EA5E"), ("", "D15EA5E"))

    def test_is_a_on_exhausted(self):
        self.assertEqual(is_a(stdstring.hexdigits)(""), ("", ""))

    def test_is_not(self):
        self.assertEqual(is_not(" \t\r\n")("Hello, World!"), (" World!", "Hello,"))

    def test_is_not_match_last(self):
        self.assertEqual(is_not(" \t\r\n")("Sometimes\t"), ("\t", "Sometimes"))

    def test_is_not_on_exhausted(self):
        self.assertEqual(is_not(" \t\r\n")(""), ("", ""))
