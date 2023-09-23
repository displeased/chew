"""
Test cases for the `generic` module.
"""
import unittest
import string as stdstring
from chew.error import Error, ErrorKind
from chew.generic import *
from chew.string import is_alphabetic


class TestGeneric(unittest.TestCase):
    def test_tag(self):
        self.assertEqual(tag("Hello")("Hello, World!"), (", World!", "Hello"))

    def test_tag_fail(self):
        with self.assertRaises(Error) as context:
            tag("Hello")("Something")

        self.assertEqual(context.exception, Error("Something", ErrorKind.TAG))

    def test_tag_on_exhausted(self):
        with self.assertRaises(Error) as context:
            tag("Hello")("")

        self.assertEqual(context.exception, Error("", ErrorKind.TAG))

    def test_take(self):
        self.assertEqual(take(6)("1234567"), ("7", "123456"))

    def test_take_overtake(self):
        with self.assertRaises(Error) as context:
            take(6)("short")

        self.assertEqual(context.exception, Error("short", ErrorKind.EOF))

    def test_take_on_exhausted(self):
        with self.assertRaises(Error) as context:
            take(6)("")

        self.assertEqual(context.exception, Error("", ErrorKind.EOF))

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

    def test_take_till1(self):
        self.assertEqual(take_till1(lambda c: c == ":")("latin:123"), (":123", "latin"))

    def test_take_till1_on_first_match(self):
        with self.assertRaises(Error) as context:
            take_till1(lambda c: c == ":")(":empty matched")

        self.assertEqual(
            context.exception, Error(":empty matched", ErrorKind.TAKE_TILL)
        )

    def test_take_till1_on_no_match(self):
        self.assertEqual(take_till1(lambda c: c == ":")("12345"), ("", "12345"))

    def test_take_till1_on_exhausted(self):
        with self.assertRaises(Error) as context:
            take_till1(lambda c: c == ":")("")
        self.assertEqual(context.exception, Error("", ErrorKind.TAKE_TILL))

    def test_take_until(self):
        self.assertEqual(take_until("eof")("hello, worldeof"), ("eof", "hello, world"))

    def test_take_until_no_match(self):
        with self.assertRaises(Error) as context:
            take_until("eof")("hello, world")
        self.assertEqual(context.exception, Error("hello, world", ErrorKind.TAKE_UNTIL))

    def test_take_until_on_exhausted(self):
        with self.assertRaises(Error) as context:
            take_until("eof")("")
        self.assertEqual(context.exception, Error("", ErrorKind.TAKE_UNTIL))

    def test_take_until_on_one_match(self):
        self.assertEqual(take_until("eof")("1eof2eof"), ("eof2eof", "1"))

    def test_take_until1(self):
        self.assertEqual(take_until1("eof")("hello, worldeof"), ("eof", "hello, world"))

    def test_take_until1_no_match(self):
        with self.assertRaises(Error) as context:
            take_until1("eof")("hello, world")
        self.assertEqual(context.exception, Error("hello, world", ErrorKind.TAKE_UNTIL))

    def test_take_until1_on_exhausted(self):
        with self.assertRaises(Error) as context:
            take_until1("eof")("")
        self.assertEqual(context.exception, Error("", ErrorKind.TAKE_UNTIL))

    def test_take_until1_on_one_match(self):
        self.assertEqual(take_until1("eof")("1eof2eof"), ("eof2eof", "1"))

    def test_take_until1_empty_result(self):
        with self.assertRaises(Error) as context:
            take_until1("eof")("eof")
        self.assertEqual(context.exception, Error("eof", ErrorKind.TAKE_UNTIL))

    def test_take_while(self):
        self.assertEqual(
            take_while(is_alphabetic)("latin123"),
            ("123", "latin"),
        )

    def test_take_while_no_match(self):
        self.assertEqual(take_while(is_alphabetic)("12345"), ("12345", ""))

    def test_take_while_all_match(self):
        self.assertEqual(take_while(is_alphabetic)("latin"), ("", "latin"))

    def test_take_while_on_exhausted(self):
        self.assertEqual(take_while(is_alphabetic)(""), ("", ""))

    def test_take_while1(self):
        self.assertEqual(
            take_while1(is_alphabetic)("latin123"),
            ("123", "latin"),
        )

    def test_take_while1_all_match(self):
        self.assertEqual(take_while1(is_alphabetic)("latin"), ("", "latin"))

    def test_take_while1_some_match(self):
        self.assertEqual(
            take_while1(is_alphabetic)("latin123"),
            ("123", "latin"),
        )

    def test_take_while1_no_match(self):
        with self.assertRaises(Error) as context:
            take_while1(is_alphabetic)("12345")
        self.assertEqual(context.exception, Error("12345", ErrorKind.TAKE_WHILE))

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
        with self.assertRaises(Error) as context:
            is_a(stdstring.hexdigits)("")

        self.assertEqual(context.exception, Error("", ErrorKind.IS_A))

    def test_is_not(self):
        self.assertEqual(is_not(" \t\r\n")("Hello, World!"), (" World!", "Hello,"))

    def test_is_not_match_last(self):
        self.assertEqual(is_not(" \t\r\n")("Sometimes\t"), ("\t", "Sometimes"))

    def test_is_not_on_exhausted(self):
        with self.assertRaises(Error) as context:
            is_not(" \t\r\n")("")

        self.assertEqual(context.exception, Error("", ErrorKind.IS_NOT))
