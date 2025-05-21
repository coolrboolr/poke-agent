from __future__ import annotations

from typing import List

from src.array_utils import Array

from src.memory.core import ContextMemory
from src.memory.short_term import GameState
from src.utils.logger import log

from .base import GameProfile


class ZeldaProfile(GameProfile):
    """Stub profile for Zelda games."""

    def parse_game_state(self, frame: Array) -> GameState:
        # Minimal mock state until perception is implemented
        return {"location": "Hyrule"}

    def get_goal_heuristics(self, context: ContextMemory) -> List[str]:
        return ["find boomerang", "defeat dungeon 1"]

    def get_reward(self, prev: GameState, curr: GameState) -> float:
        log("Zelda reward stub", tag="rl")
        return 0.0
