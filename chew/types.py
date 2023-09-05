"""
Type definitions for types.
"""
# pylint: disable=invalid-name, too-few-public-methods
from __future__ import annotations

__all__ = [
    "ParseSequence",
    "ParseElement",
    "Parser",
    "Matcher",
    "ParseResult",
]

from typing import (
    Callable,
    Sequence,
    TypeVar,
    Union,
)

# Elements of an arbitrary ParseSequence
V = TypeVar("V")

# Underlying Parser Sequence to iterate over.
#
# May be a str, bytes, or an arbitrary sequence of elements (V).
# str | bytes | Sequence[V]
ParseSequence = Union[str, bytes, Sequence[V]]

# Potential Yielded Elements of the Parse Sequence
#
# str | int | V
ParseElement = Union[str, int, V]

# Generic Parse Sequence.
S = TypeVar("S", bound=ParseSequence)

# Generic Parse Element.
E = TypeVar("E", bound=ParseElement)

# Function that evaluate the most current Element in the Parse Sequence
Matcher = Callable[[E], bool]

# Yielded Value of a Parser
T = TypeVar("T")

# Return Value of a Parser
#
# A tuple with the first element being the remaining slice to parse, and the
# second being the yielded value of the parser.
ParseResult = tuple[S, T]

# Parser
#
# A Parser is generic over its input sequence type and its return value type.
Parser = Callable[[S], ParseResult[S, T]]

# Sub-Type of a Parser that operates on Strings
StringParser = Parser[str, str]
