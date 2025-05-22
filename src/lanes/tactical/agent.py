from __future__ import annotations

import random
import time
from typing import Optional

from src.memory import GameState, ContextMemory
from src.utils.actions import Action
from src.utils.logger import log

from .battle_policy import choose_battle_move
from .pathfinder import is_player_stuck


class TacticalAgent:
    """Decision maker for battle and short-term navigation."""

    DIRECTIONS = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN]

    def __init__(self) -> None:
        self._frames = 0
        self._total_latency = 0.0

    def propose_action(
        self, game_state: GameState, context: ContextMemory
    ) -> Optional[Action]:
        """Return tactical action proposal based on game state."""
        log(f"Tactical input: {game_state}", level="DEBUG", tag="tactical")
        start = time.perf_counter()
        mode = game_state.get("mode")
        action: Optional[Action] = None

        if mode == "battle":
            battle_data = game_state.get("battle_data")
            if battle_data is None:
                log("No battle_data", level="WARN", tag="tactical")
            else:
                action = choose_battle_move(battle_data)
        else:
            if is_player_stuck(context.stm):
                action = random.choice(self.DIRECTIONS)

        elapsed = (time.perf_counter() - start) * 1000.0
        self._frames += 1
        self._total_latency += elapsed
        log(f"Proposing: {action}", tag="tactical")
        log(f"Decision latency: {elapsed:.3f}ms", level="DEBUG", tag="tactical")
        if self._frames % 100 == 0:
            avg = self._total_latency / self._frames
            log(f"Average tactical latency: {avg:.3f}ms", tag="tactical")
        return action
