"""
Error handling facilities.
"""
import dataclasses
from typing import Optional
from chew.types import Parseable


@dataclasses.dataclass
class Error(Exception):
    """
    A Parse Error.
    """

    current: Parseable
    msg: Optional[str] = None
    underlying: Optional[Exception] = None
