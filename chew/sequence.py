"""
Combinators applying parsers in sequence.
"""
# pylint: disable=invalid-name, unbalanced-tuple-unpacking
__all__ = ["multiple", "delimited", "pair", "preceded", "separated_pair", "terminated"]

from typing import Iterable, Sequence, TypeVar
from chew.types import Parser, ParseResult, S

# Generic Yielded Element
#
# Yielded element from a Parser that we care about.
Y = TypeVar("Y")

# Arbitrary Non-Returned Yielded Element
#
# Yielded element from a Parser we can discard.
A = TypeVar("A")


def multiple(parsers: Iterable[Parser[S, A]]) -> Parser[S, Sequence[A]]:
    """
    Matches a sequence of parsers.
    """

    def _multiple(sequence: S) -> ParseResult[S, Sequence[A]]:
        current = sequence
        values: list[A] = []
        for parser in parsers:
            (current, value) = parser(current)
            values.append(value)

        return (current, tuple(values))

    return _multiple


def delimited(
    left: Parser[S, A], middle: Parser[S, Y], right: Parser[S, A]
) -> Parser[S, Y]:
    """
    Matches an object from the first parser and discards it, then gets an object
    from the second parser, and finally matches an object from the third parser
    and discards it.
    """

    def _delimited(sequence: S) -> ParseResult[S, Y]:
        (current, values) = multiple([left, middle, right])(sequence)
        return (current, values[1])  # type: ignore

    return _delimited


def pair(left: Parser[S, Y], right: Parser[S, Y]) -> Parser[S, Sequence[Y]]:
    """
    Gets an object from the first parser, then another from the second.
    """
    return multiple([left, right])


def preceded(left: Parser[S, A], right: Parser[S, Y]) -> Parser[S, Y]:
    """
    Matches an object from the first parser and disacards it, then gets an
    object from the second parser.
    """

    def _preceeded(sequence: S) -> ParseResult[S, Y]:
        (current, values) = multiple([left, right])(sequence)
        return (current, values[1])  # type: ignore

    return _preceeded


def separated_pair(
    left: Parser[S, A], middle: Parser[S, Y], right: Parser[S, A]
) -> Parser[S, Sequence[Y]]:
    """
    Gets an object from the first parser, then matches an object from the middle
    parser and discards it, then gets an object from the right parser.
    """

    def _separated_pair(sequence: S) -> ParseResult[S, Sequence[Y]]:
        (current, values) = multiple([left, middle, right])(sequence)
        (lvalue, _, rvalue) = values

        return (current, (lvalue, rvalue))  # type: ignore

    return _separated_pair


def terminated(left: Parser[S, Y], right: Parser[S, A]) -> Parser[S, Y]:
    """
    Gets an object from the left parser, then gets an object from the right
    parser and discards it.
    """

    def _terminated(sequence: S) -> ParseResult[S, Y]:
        (current, values) = multiple([left, right])(sequence)
        return (current, values[0])  # type: ignore

    return _terminated
