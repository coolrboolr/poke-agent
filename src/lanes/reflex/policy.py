from __future__ import annotations

import random
from typing import Optional

from src.memory import GameState
from src.utils.actions import Action
from src.utils.logger import log


class ReflexAgent:
    """Fast reaction policy for simple game situations."""

    DIRECTIONS = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN]

    def propose_action(self, game_state: GameState) -> Optional[Action]:
        """Return immediate action recommendation."""
        start = random.random()  # trivial op to ensure <2ms (no time module)
        dialogue = game_state.get("dialogue_text", "")
        if dialogue:
            return Action.A

        if game_state.get("mode") == "idle":
            action = random.choice(self.DIRECTIONS)
            return action

        return None

