"""
Parser Wrappers for Python Literals.
"""
import string as stdstring
from chew.combine import map_res
from chew.generic import is_a
from chew.error import Error
from chew.types import Result

# Character Makeup of an Integer Literal
INT_COMPONENTS = stdstring.digits + "_"
FLOAT_COMPONENTS = stdstring.digits + "_.eE+-"


def int_literal(sequence: str) -> Result[str, int]:
    """
    Parses a decimal integer literal.
    """
    try:
        return map_res(is_a(INT_COMPONENTS), int)(sequence)
    except ValueError as error:
        raise Error(sequence) from error


def float_literal(sequence: str) -> Result[str, float]:
    """
    Parses a float literal.
    """
    try:
        return map_res(is_a(FLOAT_COMPONENTS), float)(sequence)
    except ValueError as error:
        raise Error(sequence) from error
