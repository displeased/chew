"""
Error handling facilities.
"""
# pylint: disable=raise-missing-from
from __future__ import annotations
import enum
import contextlib
import dataclasses
from chew.types import Parseable


class ErrorKind(enum.Enum):
    """
    Sub-Type of Error.
    """

    TAG = 0
    MAP_RES = 1
    MAP_OPT = 2
    ALT = 3
    IS_NOT = 4
    IS_A = 5
    SEPARATED_LIST = 6
    SEPARATED_NON_EMPTY_LIST = 7
    MANY0 = 8
    MANY1 = 9
    MANY_TILL = 10
    COUNT = 11
    TAKE_UNTIL = 12
    LENGTH_VALUE = 13
    TAG_CLOSURE = 14
    ALPHA = 15
    DIGIT = 16
    HEX_DIGIT = 17
    OCT_DIGIT = 18
    ALPHA_NUMERIC = 19
    SPACE = 20
    MULTI_SPACE = 21
    LENGTH_VALUE_FN = 22
    EOF = 23
    SWITCH = 24
    TAG_BITS = 25
    ONE_OF = 26
    NONE_OF = 27
    CHAR = 28
    CRLF = 29
    TAKE_WHILE1 = 35
    COMPLETE = 36
    FIX = 37
    ESCAPED = 38
    ESCAPED_TRANSFORM = 39
    NON_EMPTY = 40
    MANY_MN = 41
    NEGATE = 42
    PERMUTATION = 43
    VERIFY = 44
    TAKE_TILL1 = 45
    TAKE_WHILE_MN = 46
    TOO_LARGE = 47
    MANY0_COUNT = 48
    MANY1_COUNT = 49
    FLOAT = 50
    SATISFY = 51
    FAIL = 52


@dataclasses.dataclass
class Error(Exception):
    """
    An encountered error while Parsing.
    """

    remaining: Parseable
    kind: ErrorKind

    def as_int(self) -> int:
        """Gets the kind as an int."""
        return self.kind.value

    def map_kind(self, kind: ErrorKind) -> Error:
        """
        Create a new Error with the same values but a different ErrorKind.
        """
        return Error(self.remaining, kind)


@contextlib.contextmanager
def map_kind(kind: ErrorKind):
    """
    Context-manger to map the ErrorKind of a raised Error.
    """
    try:
        yield None
    except Error as error:
        raise error.map_kind(kind)


@contextlib.contextmanager
def map_exception(etype: type[Exception], remaining: Parseable, kind: ErrorKind):
    """
    Context-manager to map aribtrary exceptions to an Error.
    """
    try:
        yield None
    except Exception as exception:
        if issubclass(exception, etype) or isinstance(exception, etype):
            raise Error(remaining, kind)
        raise exception
