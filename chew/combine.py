"""
General purpose combinators.
"""
# pylint: disable=invalid-name, raise-missing-from
__all__ = [
    "all_consuming",
    "conditional",
    "consumed",
    "eof",
    "fail",
    "flat_map",
    "pariter",
    "map_res",
    "map_parser",
    "negate",
    "optional",
    "peek",
    "recognize",
    "rest",
    "rest_len",
    "success",
    "noerr_value",
    "verify",
]
from typing import TypeVar, NoReturn, Optional, Generic
import dataclasses
from chew.error import Error, ErrorKind, map_exception
from chew.types import (
    Parser,
    Result,
    Callable,
    S,
)
from chew.primitive import eof as seq_eof, take

# Arbitrary Return Element
#
# Yielded element from a Parser that we may care about.
T = TypeVar("T")

# Generic Yielded Element
#
# Yielded element from a Parser that we care about.
Y = TypeVar("Y")


@dataclasses.dataclass
class ParserIterator(Generic[S, Y]):
    """
    An Iterator constructed with a Parser over a Parseable.
    """

    current: S
    parser: Parser[S, Y]

    def __iter__(self):
        return self

    def __next__(self) -> Y:
        try:
            (new, value) = self.parser(self.current)
            self.current = new
            return value
        except Error:
            raise StopIteration

    def finish(self) -> Result[S, None]:
        """
        Get the remaining input after iteration has been exhausted.
        """
        return (self.current, None)


def all_consuming(child: Parser[S, Y]) -> Parser[S, Y]:
    """
    Succeeds if all the input has been consumed by its child parser.
    """

    def _all_consuming(sequence: S) -> Result[S, Y]:
        (current, value) = child(sequence)
        eof(current)
        return (current, value)

    return _all_consuming


def conditional(condition: bool, child: Parser[S, Y]) -> Parser[S, Optional[Y]]:
    """
    Conditionally run a child parser on the input.
    """

    def _conditional(sequence: S) -> Result[S, Optional[Y]]:
        if condition:
            return child(sequence)

        return (sequence, None)

    return _conditional


def consumed(child: Parser[S, Y]) -> Parser[S, tuple[S, Y]]:
    """
    If the child parser was successful, return the consumed input with the
    output as a tuple.
    """

    def _consumed(original: S) -> Result[S, tuple[S, Y]]:
        (remaining, value) = child(original)
        taken = len(original) - len(remaining)

        divided = take(original, taken)
        assert divided is not None

        (_, eaten) = divided
        return (remaining, (eaten, value))

    return _consumed


def eof(sequence: S) -> Result[S, S]:
    """
    Succeeds when we're at the end of the data.
    """
    if not seq_eof(sequence):
        raise Error(sequence, ErrorKind.EOF)

    return (sequence, sequence)


def fail(sequence: S) -> Result[S, NoReturn]:
    """
    Always fails.
    """
    raise Error(sequence, ErrorKind.FAIL)


def flat_map(
    parser: Parser[S, T], applied: Callable[[T], Parser[S, Y]]
) -> Parser[S, Y]:
    """
    Creates a new parser from the output of the first parser, then apply that
    parser over the rest of the input.
    """

    def _flat_map(sequence: S) -> Result[S, Y]:
        (current, intermediate) = parser(sequence)
        return applied(intermediate)(current)

    return _flat_map


def pariter(sequence: S, parser: Parser[S, Y]) -> ParserIterator[S, Y]:
    """
    Creates a Generator from input data and a parser. Stops on an Error.
    """
    return ParserIterator(sequence, parser)


def map_res(parser: Parser[S, T], mapper: Callable[[T], Y]) -> Parser[S, Y]:
    """
    Maps a function on the result of a parser.
    """

    def _map_res(sequence: S) -> Result[S, Y]:
        (current, to_convert) = parser(sequence)

        # intercept any Exception raised by our conversion function, turning it
        # into an Error with the correct ErrorKind
        with map_exception(Exception, current, ErrorKind.MAP_RES):
            value: Y = mapper(to_convert)

        return (current, value)

    return _map_res


def map_parser(parser: Parser[S, S], applied_parser: Parser[S, Y]) -> Parser[S, Y]:
    """
    Applies a parser over the result of another one.
    """

    def _map_parser(sequence: S) -> Result[S, Y]:
        (current, yielded) = parser(sequence)
        (_, value) = applied_parser(yielded)
        return (current, value)

    return _map_parser


def negate(parser: Parser[S, T]) -> Parser[S, None]:
    """
    Succeeds if the child parser returns an error.
    """

    def _negate(sequence: S) -> Result[S, None]:
        try:
            parser(sequence)
        except Error:
            return (sequence, None)
        raise Error(sequence, ErrorKind.NEGATE)

    return _negate


def optional(parser: Parser[S, T]) -> Parser[S, Optional[T]]:
    """
    Optional parser, will return None on a ParseError.
    """

    def _optional(sequence: S) -> Result[S, Optional[T]]:
        try:
            return parser(sequence)
        except Error:
            return (sequence, None)

    return _optional


def peek(parser: Parser[S, T]) -> Parser[S, T]:
    """
    Tries to apply its parser without consuming the input.
    """

    def _peek(sequence: S) -> Result[S, T]:
        (_, value) = parser(sequence)
        return (sequence, value)

    return _peek


def recognize(parser: Parser[S, T]) -> Parser[S, S]:
    """
    If the child parser was successful, return the consumed input as produced
    value.
    """

    def _recognize(sequence: S) -> Result[S, S]:
        (remaining, _) = parser(sequence)
        num_consumed = len(sequence) - len(remaining)

        divided = take(sequence, num_consumed)
        # SAFETY: We should always be able to take from the stream to the point
        # of exhaustion.
        assert divided is not None

        (_, eaten) = divided
        return (remaining, eaten)

    return _recognize


def rest(sequence: S) -> Result[S, S]:
    """
    Return the remaining input as output.
    """
    if len(sequence) == 0:
        return (sequence, sequence)

    # SAFETY: we should always be able to take from the stream.
    divided = take(sequence, len(sequence))
    assert divided is not None

    return divided


def rest_len(sequence: S) -> Result[S, int]:
    """
    Return the length of the remaining input.
    """

    return (sequence, len(sequence))


def success(value: T) -> Parser[S, T]:
    """
    Always succeeds yielding the given value.
    """

    def _success(sequence: S) -> Result[S, T]:
        return (sequence, value)

    return _success


def noerr_value(value: T, parser: Parser[S, Y]) -> Parser[S, T]:
    """
    Returns the provided value if the child parser succeeds.
    """

    def _noerr_value(sequence: S) -> Result[S, T]:
        (current, _) = parser(sequence)
        return (current, value)

    return _noerr_value


def verify(parser: Parser[S, Y], verifier: Callable[[Y], bool]) -> Parser[S, Y]:
    """
    Returns the result of the child parser if it satisfies a verification
    function.
    """

    def _verify(sequence: S) -> Result[S, Y]:
        result = parser(sequence)
        (_, value) = result

        if not verifier(value):
            raise Error(sequence, ErrorKind.VERIFY)

        return result

    return _verify
