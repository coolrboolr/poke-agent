from typing import List, Tuple
from copy import deepcopy

# Simple nested-list based array utilities

Array = List


def zeros(shape: Tuple[int, ...]) -> Array:
    """Create nested list filled with zeros."""
    if len(shape) == 0:
        return 0
    return [zeros(shape[1:]) for _ in range(shape[0])]


def ones(shape: Tuple[int, ...]) -> Array:
    """Create nested list filled with ones."""
    if len(shape) == 0:
        return 1
    return [ones(shape[1:]) for _ in range(shape[0])]


def shape(arr: Array) -> Tuple[int, ...]:
    """Return dimensions of nested list array."""
    dims = []
    sub = arr
    while isinstance(sub, list):
        dims.append(len(sub))
        if len(sub) == 0:
            break
        sub = sub[0]
    return tuple(dims)


def copy_array(arr: Array) -> Array:
    """Deep copy nested list array."""
    return deepcopy(arr)


def array_equal(a: Array, b: Array) -> bool:
    """Return True if arrays contain the same values."""
    return a == b


def sum_array(arr: Array) -> int:
    """Sum all scalar values in the array."""
    if not arr:
        return 0
    # Fast path for 3D image arrays used throughout the repo.
    if isinstance(arr[0], list) and isinstance(arr[0][0], list):
        total = 0
        for plane in arr:
            for row in plane:
                total += sum(row)
        return total
    # Fallback to generic summation for other shapes.
    if isinstance(arr[0], list):
        return sum(sum_array(sub) for sub in arr)
    return sum(arr)


def fill_rect(frame: Array, x1: int, y1: int, x2: int, y2: int, color: Tuple[int, int, int]) -> None:
    """Fill rectangular region of frame with RGB color."""
    for y in range(y1, y2):
        row = frame[y]
        for x in range(x1, x2):
            row[x] = [color[0], color[1], color[2]]

