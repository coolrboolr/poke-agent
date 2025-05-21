from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.array_utils import Array

from src.memory.core import ContextMemory
from src.memory.short_term import GameState


class GameProfile(ABC):
    """Interface for game-specific logic."""

    @abstractmethod
    def parse_game_state(self, frame: Array) -> GameState:
        """Return a GameState parsed from emulator frame."""
        raise NotImplementedError

    @abstractmethod
    def get_goal_heuristics(self, context: ContextMemory) -> List[str]:
        """Return high level goal hints for the strategic agent."""
        raise NotImplementedError

    @abstractmethod
    def get_reward(self, prev: GameState, curr: GameState) -> float:
        """Return reward signal based on state transition."""
        raise NotImplementedError
