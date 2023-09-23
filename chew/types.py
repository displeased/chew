"""
Type definitions for types.
"""
# pylint: disable=invalid-name, too-few-public-methods
from __future__ import annotations

__all__ = [
    "Parseable",
    "Element",
    "Result",
    "Parser",
    "Matcher",
]

from typing import (
    Callable,
    Sequence,
    TypeAlias,
    TypeVar,
)

# Elements of an arbitrary ParseSequence
V = TypeVar("V")

# Underlying Parser Sequence to iterate over.
#
# May be a str, bytes, or an arbitrary sequence of elements (V).
Parseable: TypeAlias = str | bytes | Sequence[V]

# Potential Yielded Elements of the Parse Sequence
Element: TypeAlias = str | int | V

# Generic Parse Sequence.
S = TypeVar("S", bound=Parseable)

# Generic Parse Element.
E = TypeVar("E", bound=Element)

# Function that evaluate the most current Element in the Parse Sequence
Matcher = Callable[[E], bool]

# Yielded Value of a Parser
T = TypeVar("T")

# Return Value of a Parser
#
# A tuple with the first element being the remaining slice to parse, and the
# second being the yielded value of the parser.
Result = tuple[S, T]

# Parser
#
# A Parser is generic over its input sequence type and its return value type.
Parser = Callable[[S], Result[S, T]]

# Sub-Type of a Parser that operates on Strings
StringParser = Parser[str, str]
