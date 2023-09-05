"""
Error handling facilities.
"""
import dataclasses
from typing import Optional
from chew.types import ParseSequence


@dataclasses.dataclass
class ParseError(Exception):
    """
    A Parse Error.
    """

    current: ParseSequence
    msg: Optional[str] = None
    underlying: Optional[Exception] = None
