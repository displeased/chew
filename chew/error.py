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
    ALT = 2
    IS_NOT = 3
    IS_A = 4
    ALPHA = 5
    DIGIT = 6
    HEX_DIGIT = 7
    OCT_DIGIT = 8
    ALPHA_NUMERIC = 9
    SPACE = 10
    MULTI_SPACE = 11
    EOF = 12
    CHAR = 13
    CRLF = 14
    NEGATE = 15
    VERIFY = 16
    SATISFY = 17
    FAIL = 18
    FLOAT = 19
    INTEGER = 20
    NONE_OF = 21
    ONE_OF = 22


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
        raise error.map_kind(kind) from error


@contextlib.contextmanager
def map_exception(etype: type[Exception], remaining: Parseable, kind: ErrorKind):
    """
    Context-manager to map aribtrary exceptions to an Error.
    """
    try:
        yield None
    except Exception as exception:
        if issubclass(etype, type(exception)) or isinstance(exception, etype):
            raise Error(remaining, kind)
        raise exception


@contextlib.contextmanager
def ignore_kind(kind: ErrorKind):
    """
    Context-Manager to ignore an ErrorKind.
    """
    try:
        yield None
    except Error as error:
        if error.kind != kind:
            raise error
