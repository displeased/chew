"""
Branch Combinators.
"""
# pylint: disable=invalid-name
__all__ = ["alt"]
from typing import Iterable, TypeVar
from chew.error import Error
from chew.types import Parser, Result, S

T = TypeVar("T")


def alt(parsers: Iterable[Parser[S, T]]) -> Parser[S, T]:
    """
    Tests a list of parsers one by one until one succeeds.
    """

    def _alt(sequence: S) -> Result[S, T]:
        for parser in parsers:
            try:
                return parser(sequence)
            except Error as _:
                pass

        raise Error(sequence)

    return _alt
