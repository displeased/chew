"""
Sparse test cases for the `comb` module.
"""
import unittest
from chew.string import alpha1, digit1, char
from chew.combine import *
from chew.branch import alt
from chew.generic import take, tag
from chew.error import ParseError
from chew.literal import int_literal
from chew.sequence import separated_pair


class TestCombine(unittest.TestCase):
    def test_all_consuming(self):
        self.assertEqual(all_consuming(alpha1)("abcd"), ("", "abcd"))

    def test_all_consuming_most_match(self):
        with self.assertRaises(ParseError):
            all_consuming(alpha1)("abcd;")

    def test_all_consuming_no_match(self):
        with self.assertRaises(ParseError):
            all_consuming(alpha1)("123abcd;")

    def test_conditional(self):
        self.assertEqual(conditional(True, alpha1)("abcd;"), (";", "abcd"))

    def test_conditional_on_false(self):
        self.assertEqual(conditional(False, alpha1)("abcd;"), ("abcd;", None))

    def test_conditional_on_true_no_match(self):
        with self.assertRaises(ParseError):
            conditional(True, alpha1)("123;")

    def test_conditional_on_false_no_match(self):
        self.assertEqual(conditional(False, alpha1)("123;"), ("123;", None))

    def test_consumed(self):
        consumed_parser = consumed(
            noerr_value(True, separated_pair(alpha1, char(","), alpha1))
        )
        self.assertEqual(consumed_parser("abcd,efgh1"), ("1", ("abcd,efgh", True)))

    def test_consumed_on_err(self):
        with self.assertRaises(ParseError):
            consumed_parser = consumed(
                noerr_value(True, separated_pair(alpha1, char(","), alpha1))
            )
            consumed_parser("abcd;")

    def test_consumed_recognized_parity_digits(self):
        def inner_parser(state):
            return noerr_value(True, tag("1234"))(state)

        recognize_parser = recognize(inner_parser)
        consumed_parser = map_res(consumed(inner_parser), lambda result: result[0])

        self.assertEqual(recognize_parser("1234"), consumed_parser("1234"))

    def test_consumed_recognized_parity_letters(self):
        def inner_parser(state):
            return noerr_value(True, tag("abcd"))(state)

        recognize_parser = recognize(inner_parser)
        consumed_parser = map_res(consumed(inner_parser), lambda result: result[0])

        self.assertEqual(recognize_parser("abcd"), consumed_parser("abcd"))

    def test_eof(self):
        with self.assertRaises(ParseError):
            eof("abc")

    def test_eof_on_empty(self):
        self.assertEqual(eof(""), ("", ""))

    def test_fail(self):
        with self.assertRaises(ParseError):
            fail("string")

    def test_flat_map(self):
        self.assertEqual(flat_map(int_literal, take)("2ab"), ("", "ab"))

    def test_flat_map_no_match(self):
        with self.assertRaises(ParseError):
            flat_map(int_literal, take)("4ab")

    def test_map_res(self):
        self.assertEqual(
            map_res(digit1, len)("123456"),
            ("", 6),
        )

    def test_map_res_no_match(self):
        with self.assertRaises(ParseError):
            map_res(digit1, len)("abc")

    def test_map_parser(self):
        self.assertEqual(map_parser(take(5), digit1)("12345"), ("", "12345"))

    def test_map_parser_on_mismatch(self):
        self.assertEqual(map_parser(take(5), digit1)("123ab"), ("", "123"))

    def test_map_parser_on_subfail(self):
        with self.assertRaises(ParseError):
            map_parser(take(5), digit1)("123")

    def test_negate(self):
        self.assertEqual(negate(alpha1)("123"), ("123", None))

    def test_negate_on_match(self):
        with self.assertRaises(ParseError):
            negate(alpha1)("abcd")

    def test_optional_on_success(self):
        self.assertEqual(optional(alpha1)("abcd;"), (";", "abcd"))

    def test_optional_on_failure(self):
        self.assertEqual(optional(alpha1)("123;"), ("123;", None))

    def test_peek(self):
        self.assertEqual(peek(alpha1)("abcd;"), ("abcd;", "abcd"))

    def test_peek_no_match(self):
        with self.assertRaises(ParseError):
            peek(alpha1)("123;")

    def test_recognize(self):
        self.assertEqual(
            recognize(separated_pair(alpha1, char(","), alpha1))("abcd,efgh"),
            ("", "abcd,efgh"),
        )

    def test_recognize_no_match(self):
        with self.assertRaises(ParseError):
            recognize(separated_pair(alpha1, char(","), alpha1))("abcd;")

    def test_rest(self):
        self.assertEqual(rest("abc"), ("", "abc"))

    def test_rest_on_exhausted(self):
        self.assertEqual(rest(""), ("", ""))

    def test_rest_len(self):
        self.assertEqual(rest_len("abc"), ("abc", 3))

    def test_rest_len_on_exhausted(self):
        self.assertEqual(rest_len(""), ("", 0))

    def test_success(self):
        self.assertEqual(success(10)("xyz"), ("xyz", 10))

    def test_success_on_complex(self):
        sign = alt((noerr_value(-1, char("-")), noerr_value(1, char("+")), success(1)))
        self.assertEqual(sign("+10"), ("10", 1))
        self.assertEqual(sign("-10"), ("10", -1))
        self.assertEqual(sign("10"), ("10", 1))

    def test_noerr_value(self):
        self.assertEqual(noerr_value(1234, alpha1)("abcd"), ("", 1234))

    def test_noerr_value_no_match(self):
        with self.assertRaises(ParseError):
            noerr_value(1234, alpha1)("123abcd;")

    def test_verify(self):
        self.assertEqual(verify(alpha1, lambda v: len(v) == 4)("abcd"), ("", "abcd"))

    def test_verify_verifier_fail(self):
        with self.assertRaises(ParseError):
            verify(alpha1, lambda v: len(v) == 4)("abcde")

    def test_verify_parser_fail(self):
        with self.assertRaises(ParseError):
            verify(alpha1, lambda v: len(v) == 4)("123abcd;")
