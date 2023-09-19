"""
Test cases for the `string` module.
"""
import unittest
from chew.string import *
from chew.types import Result
from chew.error import Error


class TestChar(unittest.TestCase):
    def test_alpha0(self):
        self.assertEqual(alpha0("ab1c"), ("1c", "ab"))

    def test_alpha0_no_match(self):
        self.assertEqual(alpha0("1c"), ("1c", ""))

    def test_alpha0_on_exhausted(self):
        self.assertEqual(alpha0(""), ("", ""))

    def test_alpha1(self):
        self.assertEqual(alpha1("aB1c"), ("1c", "aB"))

    def test_alpha1_no_match(self):
        with self.assertRaises(Error):
            alpha1("1c")

    def test_alpha1_on_exhausted(self):
        with self.assertRaises(Error):
            alpha1("")

    def test_alphanum0(self):
        self.assertEqual(alphanum0("21cZ%1"), ("%1", "21cZ"))

    def test_alphanum0_no_match(self):
        self.assertEqual(alphanum0("&Z21c"), ("&Z21c", ""))

    def test_alphanum0_on_exhausted(self):
        self.assertEqual(alphanum0(""), ("", ""))

    def test_alphanum1(self):
        self.assertEqual(alphanum1("21cZ%1"), ("%1", "21cZ"))

    def test_alphanum1_no_match(self):
        with self.assertRaises(Error):
            alphanum1("&H2")

    def test_alphanum1_on_exhausted(self):
        with self.assertRaises(Error):
            alphanum1("")

    def test_char(self):
        self.assertEqual(char("a")("abc"), ("bc", "a"))

    def test_char_no_match_space(self):
        with self.assertRaises(Error):
            char("a")(" abc")

    def test_char_no_match(self):
        with self.assertRaises(Error):
            char("a")("bc")

    def test_char_on_exhausted(self):
        with self.assertRaises(Error):
            char("a")("")

    def test_crlf(self):
        self.assertEqual(crlf("\r\nc"), ("c", "\r\n"))

    def test_crlf_no_match(self):
        with self.assertRaises(Error):
            crlf("ab\r\nc")

    def test_crlf_on_exhausted(self):
        with self.assertRaises(Error):
            crlf("")

    def test_digit0(self):
        self.assertEqual(digit0("21c"), ("c", "21"))

    def test_digit0_match_all(self):
        self.assertEqual(digit0("21"), ("", "21"))

    def test_digit0_match_none(self):
        self.assertEqual(digit0("a21c"), ("a21c", ""))

    def test_digit0_on_exhausted(self):
        self.assertEqual(digit0(""), ("", ""))

    def test_digit1(self):
        self.assertEqual(digit0("21c"), ("c", "21"))

    def test_digit1_match_none(self):
        with self.assertRaises(Error):
            digit1("c1")

    def test_digit1_on_exhausted(self):
        with self.assertRaises(Error):
            digit1("")

    def test_hex_digit0(self):
        self.assertEqual(hex_digit0("21cZ"), ("Z", "21c"))

    def test_hex_digit0_matches_none(self):
        self.assertEqual(hex_digit0("Z21c"), ("Z21c", ""))

    def test_hex_digit0_on_exhausted(self):
        self.assertEqual(hex_digit0(""), ("", ""))

    def test_hex_digit1(self):
        self.assertEqual(hex_digit1("21cZ"), ("Z", "21c"))

    def test_hex_digit1_matches_none(self):
        with self.assertRaises(Error):
            hex_digit1("H2")

    def test_hex_digit1_on_exhausted(self):
        with self.assertRaises(Error):
            hex_digit1("")

    def test_line_ending(self):
        self.assertEqual(line_ending("\r\nc"), ("c", "\r\n"))

    def test_line_ending_matches_none(self):
        with self.assertRaises(Error):
            line_ending("ab\r\nc")

    def test_line_ending_on_exhausted(self):
        with self.assertRaises(Error):
            line_ending("")

    def test_multispace0(self):
        self.assertEqual(multispace0(" \t\n\r21c"), ("21c", " \t\n\r"))

    def test_multispace0_matches_none(self):
        self.assertEqual(multispace0("Z21c"), ("Z21c", ""))

    def test_multispace0_on_exhausted(self):
        self.assertEqual(multispace0(""), ("", ""))

    def test_multispace1(self):
        self.assertEqual(multispace1(" \t\n\r21c"), ("21c", " \t\n\r"))

    def test_multispace1_matches_none(self):
        with self.assertRaises(Error):
            multispace1("H2")

    def test_multispace1_on_exhausted(self):
        with self.assertRaises(Error):
            multispace1("")

    def test_newline(self):
        self.assertEqual(newline("\nc"), ("c", "\n"))

    def test_newline_no_match(self):
        with self.assertRaises(Error):
            newline("\r\nc")

    def test_newline_on_exhausted(self):
        with self.assertRaises(Error):
            newline("")

    def test_none_of(self):
        self.assertEqual(none_of("abc")("z"), ("", "z"))

    def test_none_of_no_matches(self):
        with self.assertRaises(Error):
            none_of("ab")("a")

    def test_none_of_on_exhausted(self):
        with self.assertRaises(Error):
            none_of("a")("")

    def test_not_line_ending(self):
        self.assertEqual(not_line_ending("ab\nc"), ("\nc", "ab"))

    def test_not_line_ending_crlf(self):
        self.assertEqual(not_line_ending("ab\r\nc"), ("\r\nc", "ab"))

    def test_not_line_ending_no_match(self):
        self.assertEqual(not_line_ending("abc"), ("", "abc"))

    def test_not_line_ending_on_exhausted(self):
        self.assertEqual(not_line_ending(""), ("", ""))

    def test_oct_digit0(self):
        self.assertEqual(oct_digit0("21cZ"), ("cZ", "21"))

    def test_oct_digit0_no_match(self):
        self.assertEqual(oct_digit0("Z21c"), ("Z21c", ""))

    def test_oct_digit0_on_exhausted(self):
        self.assertEqual(oct_digit0(""), ("", ""))

    def test_oct_digit1(self):
        self.assertEqual(oct_digit1("21cZ"), ("cZ", "21"))

    def test_oct_digit1_no_match(self):
        with self.assertRaises(Error):
            oct_digit1("H2")

    def test_oct_digit1_on_exhausted(self):
        with self.assertRaises(Error):
            oct_digit1("")

    def test_one_of(self):
        self.assertEqual(one_of("abc")("b"), ("", "b"))

    def test_one_of_no_matches(self):
        with self.assertRaises(Error):
            one_of("a")("bc")

    def test_one_of_on_exhausted(self):
        with self.assertRaises(Error):
            one_of("a")("")

    def test_satisfy(self):
        self.assertEqual(satisfy(lambda c: c in "ab")("abc"), ("bc", "a"))

    def test_satisfy_no_matches(self):
        with self.assertRaises(Error):
            satisfy(lambda c: c in "ab")("cd")

    def test_satisfy_on_exhausted(self):
        with self.assertRaises(Error):
            satisfy(lambda c: c in "ab")("")

    def test_space0(self):
        self.assertEqual(space0(" \t21c"), ("21c", " \t"))

    def test_space0_no_matches(self):
        self.assertEqual(space0("Z21c"), ("Z21c", ""))

    def test_space0_on_exhausted(self):
        self.assertEqual(space0(""), ("", ""))

    def test_space1(self):
        self.assertEqual(space1(" \t21c"), ("21c", " \t"))

    def test_space1_no_matches(self):
        with self.assertRaises(Error):
            space1("H2")

    def test_space1_on_exhausted(self):
        with self.assertRaises(Error):
            space1("")

    def test_tab(self):
        self.assertEqual(tab("\tc"), ("c", "\t"))

    def test_tab_no_matches(self):
        with self.assertRaises(Error):
            tab("H2")

    def test_tab_on_exhausted(self):
        with self.assertRaises(Error):
            tab("")
