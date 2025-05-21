from __future__ import annotations

from collections import deque
from typing import Deque, Optional

from src.memory.short_term import GameState
from src.utils.actions import Action
from src.utils.logger import log


class RLCritic:
    """Very simple rolling average critic."""

    def __init__(self, window: int = 100) -> None:
        self.recent_rewards: Deque[float] = deque(maxlen=window)

    def observe(
        self, game_state: GameState, action: Optional[Action], reward: float
    ) -> None:
        """Record reward from taking `action` in `game_state`."""
        self.recent_rewards.append(reward)
        avg = sum(self.recent_rewards) / len(self.recent_rewards)
        log(f"Observed reward {reward:.2f} avg={avg:.2f}", tag="rl")

    def estimate_value(self, game_state: GameState) -> float:
        """Return critic value estimate for `game_state`."""
        if not self.recent_rewards:
            value = 0.0
        else:
            value = sum(self.recent_rewards) / len(self.recent_rewards)
        log(f"Value estimate {value:.2f}", tag="rl")
        return value
