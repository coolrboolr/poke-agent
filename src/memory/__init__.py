from __future__ import annotations

from typing import Any, Dict

GameState = Dict[str, Any]

from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from .scratchpad import WorkingMemory
from .core import ContextMemory

__all__ = [
    "GameState",
    "ShortTermMemory",
    "LongTermMemory",
    "WorkingMemory",
    "ContextMemory",
]
