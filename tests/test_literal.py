"""
Test Cases for the `literal` module.
"""

import unittest
from chew.error import ParseError
from chew.literal import int_literal, float_literal


class TestLiteral(unittest.TestCase):
    def test_int_literal(self):
        self.assertEqual(int_literal("7"), ("", 7))

    def test_int_literal_trailing(self):
        self.assertEqual(int_literal("22456a"), ("a", 22456))

    def test_int_literal_no_match(self):
        with self.assertRaises(ParseError):
            int_literal("abcdef")

    def test_int_literal_long(self):
        self.assertEqual(
            int_literal("79228162514264337593543950336"),
            ("", 79228162514264337593543950336),
        )

    def test_int_literal_underscore(self):
        self.assertEqual(int_literal("100_000_000_000"), ("", 100000000000))

    def test_float_literal(self):
        self.assertEqual(float_literal("3.14"), ("", 3.14))

    def test_float_literal_not_postfixed(self):
        self.assertEqual(float_literal("10."), ("", 10.0))

    def test_float_literal_not_prefixed(self):
        self.assertEqual(float_literal(".001"), ("", 0.001))

    def test_float_literal_exponent(self):
        self.assertEqual(float_literal("1e100"), ("", 1e100))

    def test_float_literal_exponent_complex(self):
        self.assertEqual(float_literal("3.14e-10"), ("", 3.14e-10))

    def test_float_literal_zero_exponent(self):
        self.assertEqual(float_literal("0e0"), ("", 0e0))

    def test_float_literal_underscore(self):
        self.assertEqual(float_literal("3.14_15_93"), ("", 3.14_15_93))

    def test_float_literal_no_match(self):
        with self.assertRaises(ParseError):
            float_literal("abcdef")
