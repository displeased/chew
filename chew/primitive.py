"""
Primitive Operations on Sequences.
"""
__all__ = ["eof", "peek", "take", "next_item", "at_line", "at_pos"]
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


def _consumed(original: str, remaining: str) -> str:
    """
    Returns the input that has been consumed so far.
    """
    clen = len(original) - len(remaining)
    return original[:clen]


def at_line(original: str, remaining: str) -> int:
    """
    Gets the current line number of the consumed input.
    """
    (line, _) = at_pos(original, remaining)
    return line


def at_pos(original: str, remaining: str) -> tuple[int, int]:
    """
    Gets the position of the remaining input as a tuple of the line number
    (0-indexed) and, the line character index.
    """
    consumed = _consumed(original, remaining)

    num_lines = 0
    latest_index = 0

    for i, char in enumerate(consumed):
        if char == "\n":
            num_lines += 1
            latest_index = i

    char_index = len(consumed) - latest_index
    return (num_lines, char_index)
