"""
Generic parser generators.
"""
# pylint: disable=invalid-name
__all__ = [
    "take",
    "take_till",
    "take_till1",
    "take_until",
    "take_until1",
    "take_while",
    "take_while1",
    "take_while_bounded",
    "tag",
    "is_a",
    "is_not",
]
from typing import TypeVar, Sized
from chew.error import Error, ErrorKind, map_kind
from chew.types import Parser, Matcher, Result, S
from chew.primitive import take as ptake, next_item, peek, eof

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


def take(count: int) -> Parser[S, S]:
    """
    Take count elements from the stream.

    Returns an error if the stream was exhausted in the process.
    """

    def _take(sequence: S) -> Result[S, S]:
        divided = ptake(sequence, count)
        if divided is None:
            raise Error(sequence, ErrorKind.EOF)

        return divided

    return _take


def _count_till(sequence: S, cond: Matcher, value: bool) -> int:
    """
    Counts the number of contiguous elements for which the matcher is equal to
    the desired value.
    """
    current = sequence
    count = 0
    element = peek(current)

    while (element is not None) and (cond(element) == value):
        result = next_item(current)
        assert result is not None

        count += 1
        (current, _) = result
        element = peek(current)

    return count


def take_till(cond: Matcher) -> Parser[S, S]:
    """
    Take from the state until the condition is true.
    """

    def _take_till(sequence: S) -> Result[S, S]:
        if eof(sequence):
            return (sequence, sequence)

        count = _count_till(sequence, cond, False)
        taker: Parser[S, S] = take(count)
        return taker(sequence)

    return _take_till


def take_till1(cond: Matcher) -> Parser[S, S]:
    """
    Returns the longest (minimum of 1) input slice until the condition is true.
    """
    return _min_one(take_till(cond), ErrorKind.TAKE_TILL)


def take_until(to_match: S) -> Parser[S, S]:
    """
    Returns the input slice up to the first occurrence of the pattern.
    """

    def _take_until(sequence: S) -> Result[S, S]:
        if eof(sequence):
            raise Error(sequence, ErrorKind.TAKE_UNTIL)

        longest = 0
        current: S = sequence[longest:]  # type: ignore
        exhausted = True

        while not eof(current):
            try:
                tag(to_match)(current)
                exhausted = False
                break
            except Error:
                pass
            longest += 1
            current: S = sequence[longest:]  # type: ignore

        if exhausted:
            raise Error(sequence, ErrorKind.TAKE_UNTIL)

        # SAFETY: cannot be None if we made sure that we didn't exhaust the
        # input, which we check above
        result = ptake(sequence, longest)
        assert result is not None

        return result

    return _take_until


def take_until1(to_match: S) -> Parser[S, S]:
    """
    Returns the non-empty input slice up to the first occurrence of the pattern.
    """
    return _min_one(take_until(to_match), ErrorKind.TAKE_UNTIL)


def take_while(cond: Matcher) -> Parser[S, S]:
    """
    Returns the longest input slice that matches the condition.
    """

    def _take_while(sequence: S) -> Result[S, S]:
        if eof(sequence):
            return (sequence, sequence)

        count = _count_till(sequence, cond, True)
        taker: Parser[S, S] = take(count)
        return taker(sequence)

    return _take_while


def take_while1(cond: Matcher) -> Parser[S, S]:
    """
    Returns the longest (at least 1) input slice that matches the condition.
    """
    return _min_one(take_while(cond), ErrorKind.TAKE_WHILE)


def take_while_bounded(lower: int, upper: int, cond: Matcher) -> Parser[S, S]:
    """
    Returns the longest (lower <= len <= upper) input slice that matches the predicate.
    """

    def _take_while_bounded(sequence: S) -> Result[S, S]:
        valid = 0
        maximum = min(len(sequence), upper)

        while (valid < maximum) and cond(sequence[valid]):
            valid += 1

        if valid < lower:
            raise Error(sequence, ErrorKind.TAKE_WHILE_BOUNDED)

        taker: Parser[S, S] = take(valid)
        return taker(sequence)

    return _take_while_bounded


def tag(to_match: S) -> Parser[S, S]:
    """
    Matches & Consumes a sequence of elements.
    """

    def _tag(sequence: S) -> Result[S, S]:
        taker: Parser[S, S] = take(len(to_match))
        with map_kind(ErrorKind.TAG):
            (current, next_items) = taker(sequence)

        for expected, existing in zip(to_match, next_items):
            if existing != expected:
                raise Error(sequence, ErrorKind.TAG)

        return (current, to_match)

    return _tag


def is_a(items: S) -> Parser[S, S]:
    """
    Returns the longest slice whose elements are in the sequence of items.
    """

    def _is_a(sequence: S) -> Result[S, S]:
        with map_kind(ErrorKind.IS_A):
            taker: Parser[S, S] = take_while1(lambda el: el in items)
            return taker(sequence)

    return _is_a


def is_not(items: S) -> Parser[S, S]:
    """
    Returns the longest slice whose elements do not contain the sequence of
    items.
    """

    def _is_not(sequence: S) -> Result[S, S]:
        with map_kind(ErrorKind.IS_NOT):
            taker: Parser[S, S] = take_while1(lambda el: el not in items)
            return taker(sequence)

    return _is_not
