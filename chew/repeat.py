"""
Combinators applying their child parser multiple times.
"""
__all__ = [
    "count",
    "fill",
    "fold_many0",
    "fold_many1",
    "length_count",
    "length_data",
    "length_value",
]
# pylint: disable=invalid-name
from typing import MutableSequence, Callable, Sequence, TypeVar
from chew.types import Parser, Result, S
from chew.error import Error, ErrorKind
from chew.generic import take, _min_one, I
from chew.primitive import eof

# Generic Yielded Element
#
# Yielded element from a Parser that we care about.
Y = TypeVar("Y")

# Arbitrary
#
# Aribtrary Held Value.
A = TypeVar("A")


def count(parser: Parser[S, Y], times: int) -> Parser[S, Sequence[Y]]:
    """
    Repeat a Parser parser "times" times, collecting the results into a list.
    """

    def _count(sequence: S) -> Result[S, Sequence[Y]]:
        values: list[Y] = []
        current = sequence

        for _ in range(times):
            (current, value) = parser(current)
            values.append(value)

        return (current, values)

    return _count


def fill(parser: Parser[S, Y], buffer: MutableSequence[Y]) -> Parser[S, None]:
    """
    Fill the given buffer with the results of running the parser.
    """

    def _fill(sequence: S) -> Result[S, None]:
        current = sequence
        for i, _ in enumerate(buffer):
            (current, value) = parser(current)
            buffer[i] = value

        return (current, None)

    return _fill


def fold_many0(
    parser: Parser[S, Y], constructor: Callable[[], A], gather: Callable[[A, Y], A]
):
    """
    Repeats the parser, calling `gather` to gather the results.

    Constructs an accumulator A using the passed constructor `constr`. For each
    yielded element, calls `gather` to modify the accumulator.

    Returns on an exhausted sequence to prevent an infinite loop with parsers
    that accept empty inputs.
    """

    def _fold_many0(sequence: S) -> Result[S, A]:
        accumulator: A = constructor()
        current = sequence

        while True:
            if eof(sequence):
                break

            try:
                (current, value) = parser(current)
                accumulator = gather(accumulator, value)
            except Error:
                break

        return (current, accumulator)

    return _fold_many0


def fold_many1(
    parser: Parser[S, Y], constructor: Callable[[], I], gather: Callable[[I, Y], I]
):
    """
    Repeats the parser, calling `gather` to gather the results.

    Constructs an accumulator A using the passed constructor `constr`. For each
    yielded element, calls `gather` to modify the accumulator.

    Returns on an exhausted sequence to prevent an infinite loop with parsers
    that accept empty inputs.
    """
    return _min_one(fold_many0(parser, constructor, gather), ErrorKind.MANY1)


def length_count(
    num_parser: Parser[S, int], repeat: Parser[S, Y]
) -> Parser[S, Sequence[Y]]:
    """
    Gets a number from the first parser, then applies the second parser that
    many times.
    """

    def _length_count(sequence: S) -> Result[S, Sequence[Y]]:
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

    def _length_data(sequence: S) -> Result[S, S]:
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

    def _length_value(sequence: S) -> Result[S, Y]:
        current = sequence

        (current, subslice) = length_data(num_parser)(current)
        (_, result) = slice_parser(subslice)

        return (current, result)

    return _length_value
