"""
Combinators applying their child parser multiple times.
"""
__all__ = ["count", "length_count", "length_data", "length_value"]
# pylint: disable=invalid-name
from typing import Sequence, TypeVar
from chew.types import Parser, ParseResult, S
from chew.generic import take

# Generic Yielded Element
#
# Yielded element from a Parser that we care about.
Y = TypeVar("Y")


def count(parser: Parser[S, Y], times: int) -> Parser[S, Sequence[Y]]:
    """
    Repeat a Parser parser "times" times, collecting the results into a list.
    """

    def _count(sequence: S) -> ParseResult[S, Sequence[Y]]:
        values: list[Y] = []
        current = sequence

        for _ in range(times):
            (current, value) = parser(current)
            values.append(value)

        return (current, values)

    return _count


def length_count(
    num_parser: Parser[S, int], repeat: Parser[S, Y]
) -> Parser[S, Sequence[Y]]:
    """
    Gets a number from the first parser, then applies the second parser that
    many times.
    """

    def _length_count(sequence: S) -> ParseResult[S, Sequence[Y]]:
        results: list[Y] = []
        current = sequence

        (current, times) = num_parser(current)
        # SAFETY: the number parser MUST return an integer of some sort!
        assert isinstance(times, int)

        for _ in range(times):
            (current, result) = repeat(current)
            results.append(result)

        return (current, results)

    return _length_count


def length_data(num_parser: Parser[S, int]) -> Parser[S, S]:
    """
    Gets a number from the parser and returns a subslice of the input of that
    size.
    """

    def _length_data(sequence: S) -> ParseResult[S, S]:
        current = sequence

        (current, times) = num_parser(current)
        # SAFETY: the number parser MUST return an integer of some sort!
        assert isinstance(times, int)

        taker: Parser[S, S] = take(times)
        return taker(current)

    return _length_data


def length_value(
    num_parser: Parser[S, int], slice_parser: Parser[S, Y]
) -> Parser[S, Y]:
    """
    Gets a number from the first parser, takes a subslice of the input of that
    size, then applies the second parser on that subslice.
    """

    def _length_value(sequence: S) -> ParseResult[S, Y]:
        current = sequence

        (current, subslice) = length_data(num_parser)(current)
        (_, result) = slice_parser(subslice)

        return (current, result)

    return _length_value
