from __future__ import annotations

from typing import Any

from src.memory.short_term import ShortTermMemory


def is_player_stuck(stm: ShortTermMemory) -> bool:
    """Return True if the player's position hasn't changed in recent frames."""
    frames = stm.get_last(5)
    if len(frames) < 2:
        return False
    positions = [f.get("position") for f in frames if "position" in f]
    if len(positions) < len(frames):
        return False
    first = positions[0]
    return all(pos == first for pos in positions[1:])
