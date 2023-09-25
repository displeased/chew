"""
Test Cases for the `error` module.
"""

import unittest
from tests import assert_error
from chew.error import *


class TestError(unittest.TestCase):
    def test_error_int_conversion(self):
        self.assertEqual(Error("", ErrorKind.TAG).as_int(), ErrorKind.TAG.value)

    def test_map_exception(self):
        with assert_error(self, Error("", ErrorKind.EOF)):
            with map_exception(ValueError, "", ErrorKind.EOF):
                raise ValueError()

    def test_map_exception_no_match(self):
        with self.assertRaises(ValueError):
            with map_exception(IndexError, "", ErrorKind.EOF):
                raise ValueError()

    def test_ignore_kind(self):
        with ignore_kind(ErrorKind.EOF):
            raise Error("", ErrorKind.EOF)

    def test_ignore_kind_no_match(self):
        with assert_error(self, Error("", ErrorKind.ALPHA)):
            with ignore_kind(ErrorKind.EOF):
                raise Error("", ErrorKind.ALPHA)
