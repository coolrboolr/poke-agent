from __future__ import annotations

from typing import List

from src.array_utils import Array

from src.perception.runner import PerceptionRunner
from src.memory.core import ContextMemory
from src.memory.short_term import GameState
from src.utils.logger import log

from .base import GameProfile


class PokemonProfile(GameProfile):
    """Game profile for Pokémon games using existing perception and reward."""

    def __init__(self) -> None:
        self.runner = PerceptionRunner()

    def parse_game_state(self, frame: Array) -> GameState:
        return self.runner.process_frame(frame)

    def get_goal_heuristics(self, context: ContextMemory) -> List[str]:
        return ["pewter", "brock"]

    def get_reward(self, prev: GameState, curr: GameState) -> float:
        reward = 0.0
        if curr.get("badges", 0) > prev.get("badges", 0):
            reward += 10.0
            log("Badge gained +10", tag="rl")
        if (
            prev.get("in_battle")
            and not curr.get("in_battle")
            and curr.get("battle_result") == "win"
        ):
            reward += 5.0
            log("Battle win +5", tag="rl")
        if curr.get("fainted") or curr.get("stuck"):
            reward -= 10.0
            log("Penalty -10", tag="rl")
        return reward
