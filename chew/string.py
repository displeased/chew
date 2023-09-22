"""
Parsers that operate on strings.
"""
# pylint: disable=invalid-name
__all__ = [
    "satisfy",
    "char",
    "alpha0",
    "alpha1",
    "alphanum0",
    "alphanum1",
    "crlf",
    "digit0",
    "digit1",
    "hex_digit0",
    "hex_digit1",
    "line_ending",
    "multispace0",
    "multispace1",
    "newline",
    "none_of",
    "not_line_ending",
    "oct_digit0",
    "oct_digit1",
    "one_of",
    "space0",
    "space1",
    "tab",
    "tag_no_case",
]
from typing import Sequence, TypeVar, Sized
import string as stdstring
from chew.types import (
    StringParser,
    Result,
    Matcher,
    Parser,
    S,
)
from chew.error import Error, ErrorKind, map_kind, ignore_kind
from chew.branch import alt
from chew.generic import tag, is_a, take, take_while

# Sized Yielded Element
#
# Yielded value from a parser that has a size.
I = TypeVar("I", bound=Sized)


def _min_one(wrapped: Parser[S, I], error: ErrorKind) -> Parser[S, I]:
    """
    Wraps the provided parser and raises an exception with the given kind if the
    returned Parser result does not have at least one element.
    """

    def __min_one(sequence: S) -> Result[S, I]:
        result = wrapped(sequence)
        (_, match) = result

        if len(match) == 0:
            raise Error(sequence, error)

        return result

    return __min_one


def tag_no_case(to_match: str) -> StringParser:
    """
    Recognizes a Case-Insensitive Pattern.
    """

    def _tag_no_case(sequence: str) -> Result[str, str]:
        taker: Parser[str, str] = take(len(to_match))
        with map_kind(ErrorKind.TAG):
            (current, raw_compare) = taker(sequence)

        if to_match.lower() != raw_compare.lower():
            raise Error(sequence, ErrorKind.TAG)

        return (current, raw_compare)

    return _tag_no_case


def char(character: str) -> StringParser:
    """
    Matches a single character.
    """

    def _char(sequence: str) -> Result[str, str]:
        taker: Parser[str, str] = take(1)
        with map_kind(ErrorKind.CHAR):
            result = taker(sequence)
        (_, nchar) = result

        if nchar != character:
            raise Error(sequence, ErrorKind.CHAR)

        return result

    return _char


def satisfy(cond: Matcher) -> StringParser:
    """
    Recognizes one character and check that it satisfies a predicate.
    """

    def _satisfy(sequence: str) -> Result:
        taker: Parser[str, str] = take(1)
        with map_kind(ErrorKind.SATISFY):
            (current, item) = taker(sequence)
        if cond(item):
            return (current, item)
        raise Error(sequence, ErrorKind.SATISFY)

    return _satisfy


def one_of(characters: Sequence[str]) -> StringParser:
    """
    Recognizes one of the provided characters.
    """

    def _one_of(sequence: str) -> Result[str, str]:
        with map_kind(ErrorKind.ONE_OF):
            return satisfy(lambda c: c in characters)(sequence)

    return _one_of


def none_of(characters: Sequence[str]) -> StringParser:
    """
    Recognizes a character that is not in the provided characters.
    """

    def _none_of(sequence: str) -> Result[str, str]:
        with map_kind(ErrorKind.NONE_OF):
            return satisfy(lambda c: c not in characters)(sequence)

    return _none_of


def alpha0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more uppercase alphabetic characters.
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(stdstring.ascii_letters)(sequence)
    return (sequence, "")


def alpha1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more alphabetic characters.
    """
    return _min_one(alpha0, ErrorKind.ALPHA)(sequence)


def alphanum0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more alphanumeric characters.
    """

    # SAFETY: element type constraint will be enforced on calling our return
    # value
    return take_while(str.isalnum)(sequence)  # type: ignore


def alphanum1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more alphanumeric characters.
    """

    return _min_one(alphanum0, ErrorKind.ALPHA_NUMERIC)(sequence)


def crlf(sequence: str) -> Result[str, str]:
    """
    Matches an "\\r\\n".
    """
    with map_kind(ErrorKind.CRLF):
        return tag("\r\n")(sequence)


def digit0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more ASCII numerical characters (0 - 9).
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(stdstring.digits)(sequence)
    return (sequence, "")


def digit1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more ASCII numerical characters (0 - 9).
    """

    return _min_one(digit0, ErrorKind.DIGIT)(sequence)


def hex_digit0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more ASCII hexidecimal characters (0-9, A-F, a-f).
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(stdstring.hexdigits)(sequence)
    return (sequence, "")


def hex_digit1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more ASCII hexidecimal characters (0-9, A-F, a-f).
    """
    return _min_one(hex_digit0, ErrorKind.HEX_DIGIT)(sequence)


def line_ending(sequence: str) -> Result[str, str]:
    """
    Recognizes an end of line (both '\\n' and '\\r\\n').
    """
    with map_kind(ErrorKind.CRLF):
        return alt([char("\n"), tag("\r\n")])(sequence)


def multispace0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more spaces, tabs, carriage returns, and line feeds.
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(" \t\n\r")(sequence)
    return (sequence, "")


def multispace1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more spaces, tabs, carriage returns, and line feeds.
    """
    return _min_one(multispace0, ErrorKind.MULTI_SPACE)(sequence)


def newline(sequence: str) -> Result[str, str]:
    """
    Matches a newline character '\\n'.
    """
    return char("\n")(sequence)


def not_line_ending(sequence: str) -> Result[str, str]:
    """
    Recognizes a string of any character except '\\r\\n' or '\\n'.
    """
    return take_while(lambda el: el not in "\r\n")(sequence)  # type: ignore


def oct_digit0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more octal characters (0-7).
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(stdstring.octdigits)(sequence)
    return (sequence, "")


def oct_digit1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more octal characters (0-7).
    """
    return _min_one(oct_digit0, ErrorKind.OCT_DIGIT)(sequence)


def space0(sequence: str) -> Result[str, str]:
    """
    Recognizes zero or more spaces and tabs.
    """
    with ignore_kind(ErrorKind.IS_A):
        return is_a(" \t")(sequence)
    return (sequence, "")


def space1(sequence: str) -> Result[str, str]:
    """
    Recognizes one or more spaces and tabs.
    """
    return _min_one(space0, ErrorKind.SPACE)(sequence)


def tab(sequence: str) -> Result[str, str]:
    """
    Matches a tab character.
    """
    return char("\t")(sequence)
