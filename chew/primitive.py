"""
Primitive Operations on Sequences.
"""
__all__ = ["eof", "peek", "take", "next_item", "at_line"]
from typing import Optional
from chew.types import S, E


def eof(sequence: S) -> bool:
    """
    Whether or not a ParseSequence has been exhausted.
    """
    return len(sequence) == 0


def peek(sequence: S) -> Optional[E]:
    """
    Peeks at the next item without consuming it.
    """
    if eof(sequence):
        return None

    item: E = sequence[0]  # type: ignore
    return item


def take(sequence: S, count: int) -> Optional[tuple[S, S]]:
    """
    Take a `count` number of elements from the sequence, subdividing into two
    separate sequences.
    """
    size: int = len(sequence)
    if (size == 0) or (size < count):
        return None

    # SAFETY: up-to slicing will never raise an IndexError even with values of
    # count that extend beyond the length of the sequence.
    yielded: S = sequence[:count]  # type: ignore
    remaining: S = sequence[count:]  # type: ignore

    return (remaining, yielded)


def next_item(sequence: S) -> Optional[tuple[S, E]]:
    """
    Yields the next item in a sequence and the remaining sequence if possible.
    """
    if eof(sequence):
        return None

    # SAFETY: these types should correlate
    current: E = sequence[0]  # type: ignore
    leftover: S = sequence[1:]  # type: ignore

    return (leftover, current)


def at_line(original: str, remaining: str) -> int:
    """
    Counts the number of newlines in the derived consumed stream to get the
    current Line Index (Display Line Number = Line Index + 1).
    """
    consumed_len: int = len(original) - len(remaining)
    consumed = original[:consumed_len]

    newlines = 0
    for char in consumed:
        if char == "\n":
            newlines += 1

    return newlines
