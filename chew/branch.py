"""
Branch Combinators.
"""
# pylint: disable=invalid-name
__all__ = ["alt"]
from typing import Iterable, TypeVar
from chew.error import ParseError
from chew.types import Parser, ParseResult, S

T = TypeVar("T")


def alt(parsers: Iterable[Parser[S, T]]) -> Parser[S, T]:
    """
    Tests a list of parsers one by one until one succeeds.
    """

    def _alt(sequence: S) -> ParseResult[S, T]:
        for parser in parsers:
            try:
                return parser(sequence)
            except ParseError as _:
                pass

        raise ParseError(sequence)

    return _alt
