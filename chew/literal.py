"""
Parser Wrappers for Python Literals.
"""
import string as stdstring
from chew.combine import map_res
from chew.generic import is_a
from chew.error import ErrorKind, map_exception
from chew.types import Result

# Character Makeup of an Integer Literal
INT_COMPONENTS = stdstring.digits + "_"
FLOAT_COMPONENTS = stdstring.digits + "_.eE+-"


def int_literal(sequence: str) -> Result[str, int]:
    """
    Parses a decimal integer literal.
    """
    with map_exception(ValueError, sequence, ErrorKind.INTEGER):
        return map_res(is_a(INT_COMPONENTS), int)(sequence)


def float_literal(sequence: str) -> Result[str, float]:
    """
    Parses a float literal.
    """
    with map_exception(ValueError, sequence, ErrorKind.FLOAT):
        return map_res(is_a(FLOAT_COMPONENTS), float)(sequence)
