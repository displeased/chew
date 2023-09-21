"""
Test Cases for the `error` module.
"""

import unittest
from chew.error import *


class TestError(unittest.TestCase):
    def test_error_int_conversion(self):
        self.assertEqual(Error("", ErrorKind.TAG).as_int(), ErrorKind.TAG.value)

    def test_map_exception(self):
        with self.assertRaises(Error) as raised:
            with map_exception(ValueError, "", ErrorKind.EOF):
                raise ValueError()

        self.assertEqual(raised.exception.kind, ErrorKind.EOF)
        self.assertEqual(raised.exception.remaining, "")

    def test_map_exception_no_match(self):
        with self.assertRaises(ValueError):
            with map_exception(IndexError, "", ErrorKind.EOF):
                raise ValueError()

    def test_ignore_kind(self):
        with ignore_kind(ErrorKind.EOF):
            raise Error("", ErrorKind.EOF)

    def test_ignore_kind_no_match(self):
        with self.assertRaises(Error) as raised:
            with ignore_kind(ErrorKind.EOF):
                raise Error("", ErrorKind.ALPHA)

        self.assertEqual(raised.exception.kind, ErrorKind.ALPHA)
        self.assertEqual(raised.exception.remaining, "")
