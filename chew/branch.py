"""
Branch Combinators.
"""
# pylint: disable=invalid-name
__all__ = ["alt"]
from typing import Iterable, Optional, TypeVar
from chew.error import Error, ErrorKind
from chew.types import Parser, Result, S

# Shared Alternative Parser Return Value
#
# Generic return type of any given Parser passed to alt.
T = TypeVar("T")


def alt(parsers: Iterable[Parser[S, T]]) -> Parser[S, T]:
    """
    Tests a list of parsers one by one until one succeeds.
    """

    def _alt(sequence: S) -> Result[S, T]:
        last_error: Optional[Error] = None
        for parser in parsers:
            try:
                return parser(sequence)
            except Error as error:
                last_error = error

        if last_error is not None:
            raise last_error
        raise Error(sequence, ErrorKind.ALT)

    return _alt
