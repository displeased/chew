"""
Combinators applying their child parser multiple times.
"""
__all__ = [
    "count",
    "fill",
    "fold_many0",
    "fold_many1",
    "fold_many_bounded",
    "length_count",
    "length_data",
    "length_value",
    "many0",
    "many0_count",
    "many1",
    "many1_count",
    "many_bounded",
    "many_till",
]
# pylint: disable=invalid-name
from typing import MutableSequence, Callable, Sequence, TypeVar, Optional
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
) -> Parser[S, A]:
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
            if eof(current):
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


def fold_many_bounded(
    lower: int,
    upper: int,
    parser: Parser[S, Y],
    constructor: Callable[[], A],
    gather: Callable[[A, Y], A],
):
    """
    Repeats the parser, calling `gather` to gather the results.
    """

    def _fold_many_bounded(sequence: S) -> Result[S, A]:
        accumulator: A = constructor()
        current = sequence
        runs = 0

        while runs < upper:
            try:
                (current, value) = parser(current)
                accumulator = gather(accumulator, value)
                runs += 1
            except Error:
                break

        if runs < lower:
            raise Error(sequence, ErrorKind.FOLD_MANY_BOUNDED)

        return (current, accumulator)

    return _fold_many_bounded


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


def many0(parser: Parser[S, Y]) -> Parser[S, Sequence[Y]]:
    """
    Repeats the parser, calling the results into a Sequence.

    Returns on an exhausted sequence to prevent an infinite loop with parsers
    that accept empty inputs.
    """

    def lappend(acc: list[Y], item: Y) -> list[Y]:
        acc.append(item)
        return acc

    return fold_many0(parser, list, lappend)  # type: ignore


def many0_count(parser: Parser[S, Y]) -> Parser[S, int]:
    """
    Repeats the embedded parser, counting the number of successes before a
    failure.
    """

    def _many0_count(sequence: S) -> Result[S, int]:
        consecutive = 0
        current = sequence
        while True:
            if eof(current):
                break
            try:
                (current, _) = parser(current)
                consecutive += 1
            except Error:
                break

        return (current, consecutive)

    return _many0_count


def many1(parser: Parser[S, Y]) -> Parser[S, Sequence[Y]]:
    """
    Runs the embedded Parser, raising an Error if the embedded Parser does not
    exit with a success at least once.
    """

    def _many1(sequence: S) -> Result[S, Sequence[Y]]:
        once = False
        result = []
        current = sequence
        last_raised: Optional[Error] = None

        while True:
            try:
                (current, value) = parser(current)
                result.append(value)
                once = True
            except Error as error:
                last_raised = error
                break
            if eof(current):
                break

        if not once:
            kind = ErrorKind.MANY1
            if last_raised is not None:
                kind = last_raised.kind
            raise Error(sequence, kind)

        return (current, result)

    return _many1


def many1_count(parser: Parser[S, Y]) -> Parser[S, int]:
    """
    Runs the Parser as many time as possible, counting the results.
    """

    def _many1_count(sequence: S) -> Result[S, int]:
        result = many0_count(parser)(sequence)

        (_, icount) = result
        if icount < 1:
            raise Error(sequence, ErrorKind.MANY1_COUNT)

        return result

    return _many1_count


def many_bounded(
    lower: int, upper: int, parser: Parser[S, Y]
) -> Parser[S, Sequence[Y]]:
    """
    Repeats the parser within the given bounds.
    """

    def _many_bounded(sequence: S) -> Result[S, Sequence[Y]]:
        result = []
        matches = 0
        current = sequence
        while True:
            try:
                if eof(current):
                    break
                (current, value) = parser(current)
                result.append(value)
                matches += 1
            except Error:
                break
            if matches == upper:
                break

        if matches < lower:
            raise Error(sequence, ErrorKind.MANY_BOUNDED)

        return (current, result)

    return _many_bounded


def many_till(
    applied: Parser[S, Y], marker: Parser[S, A]
) -> Parser[S, tuple[Sequence[Y], A]]:
    """
    Applies the parser `applied` until the `marker` parser yields a result.
    """

    def _many_till(sequence: S) -> Result[S, tuple[Sequence[Y], A]]:
        current = sequence
        results = []
        while True:
            try:
                (current, trailing) = marker(current)
                break
            except Error:
                pass

            (current, value) = applied(current)
            results.append(value)

        return (current, (results, trailing))

    return _many_till
