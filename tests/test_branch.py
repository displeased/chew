"""
Test cases for the `branch` module.
"""

import unittest
from tests import assert_error
from chew.string import alpha1, digit1
from chew.error import Error, ErrorKind
from chew.branch import alt


class TestBranch(unittest.TestCase):
    def test_alt_all_one(self):
        self.assertEqual(alt((alpha1, digit1))("abc"), ("", "abc"))

    def test_alt_all_other(self):
        self.assertEqual(alt((alpha1, digit1))("123456"), ("", "123456"))

    def test_alt_both_fail(self):
        with assert_error(self, Error(" ", ErrorKind.DIGIT)):
            alt((alpha1, digit1))(" ")
