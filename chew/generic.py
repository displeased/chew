"""
Generic parser generators.
"""
__all__ = ["take", "take_till", "take_while", "tag", "is_a", "is_not"]
from chew.error import Error, ErrorKind
from chew.types import Parser, Matcher, Result, S
from chew.primitive import take as ptake, next_item, peek, eof


def take(count: int) -> Parser[S, S]:
    """
    Take count elements from the stream.

    Returns an error if the stream was exhausted in the process.
    """

    def _take(sequence: S) -> Result[S, S]:
        if len(sequence) < count:
            raise Error(sequence, ErrorKind.EOF)

        # SAFETY: result should never be None when the above precondition is
        # checked
        result = ptake(sequence, count)
        assert result is not None

        return result

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


def take_while(cond: Matcher) -> Parser[S, S]:
    """
    Take from the state while the condition is true.
    """

    def _take_while(sequence: S) -> Result:
        if eof(sequence):
            return (sequence, sequence)

        count = _count_till(sequence, cond, True)
        taker: Parser[S, S] = take(count)
        return taker(sequence)

    return _take_while


def tag(to_match: S) -> Parser[S, S]:
    """
    Matches & Consumes a sequence of elements.
    """

    def _tag(sequence: S) -> Result[S, S]:
        taker: Parser[S, S] = take(len(to_match))
        (current, next_items) = taker(sequence)

        for expected, existing in zip(to_match, next_items):
            if existing != expected:
                raise Error(current, ErrorKind.TAG)

        return (current, to_match)

    return _tag


def is_a(items: S) -> Parser[S, S]:
    """
    Returns the longest slice whose elements are in the sequence of items.
    """

    def _is_a(sequence: S) -> Result[S, S]:
        taker: Parser[S, S] = take_while(lambda el: el in items)
        return taker(sequence)

    return _is_a


def is_not(items: S) -> Parser[S, S]:
    """
    Returns the longest slice whose elements do not contain the sequence of
    items.
    """

    def _is_not(sequence: S) -> Result[S, S]:
        taker: Parser[S, S] = take_while(lambda el: el not in items)
        return taker(sequence)

    return _is_not
