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
]
from typing import Sequence, TypeVar, Sized
import string as stdstring
from chew.types import (
    StringParser,
    ParseResult,
    Matcher,
    Parser,
    S,
)
from chew.error import ParseError
from chew.branch import alt
from chew.generic import tag, is_a, take, take_while

# Sized Yielded Element
#
# Yielded value from a parser that has a size.
I = TypeVar("I", bound=Sized)


def _min_one(wrapped: Parser[S, I]) -> Parser[S, I]:
    """
    A ParseResult with a sequence as its return value must have at least one
    element.
    """

    def __min_one(sequence: S) -> ParseResult[S, I]:
        result = wrapped(sequence)
        (_, match) = result

        if len(match) == 0:
            raise ParseError(sequence)

        return result

    return __min_one


def char(character: str) -> StringParser:
    """
    Matches a single character.
    """

    def _char(sequence: str) -> ParseResult[str, str]:
        taker: Parser[str, str] = take(1)
        result = taker(sequence)
        (_, nchar) = result

        if nchar != character:
            raise ParseError(sequence)

        return result

    return _char


def satisfy(cond: Matcher) -> StringParser:
    """
    Recognizes one character and check that it satisfies a predicate.
    """

    def _satisfy(sequence: str) -> ParseResult:
        taker: Parser[str, str] = take(1)
        (current, item) = taker(sequence)
        if cond(item):
            return (current, item)
        raise ParseError(current)

    return _satisfy


def one_of(characters: Sequence[str]) -> StringParser:
    """
    Recognizes one of the provided characters.
    """

    return satisfy(lambda c: c in characters)


def none_of(characters: Sequence[str]) -> StringParser:
    """
    Recognizes a character that is not in the provided characters.
    """

    return satisfy(lambda c: c not in characters)


def alpha0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more uppercase alphabetic characters.
    """
    return is_a(stdstring.ascii_letters)(sequence)


def alpha1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more alphabetic characters.
    """

    return _min_one(alpha0)(sequence)


def alphanum0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more alphanumeric characters.
    """

    # SAFETY: element type constraint will be enforced on calling our return
    # value
    return take_while(str.isalnum)(sequence)  # type: ignore


def alphanum1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more alphanumeric characters.
    """

    return _min_one(alphanum0)(sequence)


def crlf(sequence: str) -> ParseResult[str, str]:
    """
    Matches an "\\r\\n".
    """
    return tag("\r\n")(sequence)


def digit0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more ASCII numerical characters (0 - 9).
    """

    return is_a(stdstring.digits)(sequence)


def digit1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more ASCII numerical characters (0 - 9).
    """

    return _min_one(digit0)(sequence)


def hex_digit0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more ASCII hexidecimal characters (0-9, A-F, a-f).
    """

    return is_a(stdstring.hexdigits)(sequence)


def hex_digit1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more ASCII hexidecimal characters (0-9, A-F, a-f).
    """
    return _min_one(hex_digit0)(sequence)


def line_ending(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes an end of line (both '\\n' and '\\r\\n').
    """
    return alt([char("\n"), tag("\r\n")])(sequence)


def multispace0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more spaces, tabs, carriage returns, and line feeds.
    """
    return is_a(" \t\n\r")(sequence)


def multispace1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more spaces, tabs, carriage returns, and line feeds.
    """
    return _min_one(multispace0)(sequence)


def newline(sequence: str) -> ParseResult[str, str]:
    """
    Matches a newline character '\\n'.
    """
    return char("\n")(sequence)


def not_line_ending(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes a string of any character except '\\r\\n' or '\\n'.
    """
    return take_while(lambda el: el not in "\r\n")(sequence)  # type: ignore


def oct_digit0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more octal characters (0-7).
    """
    return is_a(stdstring.octdigits)(sequence)


def oct_digit1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more octal characters (0-7).
    """
    return _min_one(oct_digit0)(sequence)


def space0(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes zero or more spaces and tabs.
    """
    return is_a(" \t")(sequence)


def space1(sequence: str) -> ParseResult[str, str]:
    """
    Recognizes one or more spaces and tabs.
    """
    return _min_one(space0)(sequence)


def tab(sequence: str) -> ParseResult[str, str]:
    """
    Matches a tab character.
    """
    return char("\t")(sequence)
