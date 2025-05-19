from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List

from src.utils.logger import log

GameState = Dict[str, Any]


class ShortTermMemory:
    """Buffer recent GameState objects."""

    def __init__(self, maxlen: int = 120) -> None:
        self.buffer: Deque[GameState] = deque(maxlen=maxlen)

    def append(self, frame: GameState) -> None:
        """Add a new GameState and log scene transitions."""
        if self.buffer:
            last = self.buffer[-1]
            if (
                frame.get("location_id") != last.get("location_id")
                or frame.get("mode") != last.get("mode")
            ):
                log("Scene transition detected", tag="memory")
        self.buffer.append(frame)
        log("Frame appended to STM", tag="memory")

    def get_last(self, n: int) -> List[GameState]:
        """Return the last n GameState entries."""
        if n <= 0:
            return []
        return list(self.buffer)[-n:]
