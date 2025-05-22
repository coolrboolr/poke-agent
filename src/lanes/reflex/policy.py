from __future__ import annotations

import random
import time
from typing import Optional

from src.memory import GameState
from src.utils.actions import Action
from src.utils.logger import log


class ReflexAgent:
    """Fast reaction policy for simple game situations."""

    DIRECTIONS = [Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN]

    def __init__(self, default_mode: str = "explore") -> None:
        self._frames = 0
        self._total_latency = 0.0
        self.default_mode = default_mode
        self._warned_missing_mode = False

    def propose_action(self, game_state: GameState) -> Optional[Action]:
        """Return immediate action recommendation."""
        start = time.perf_counter()

        log(f"Reflex input: {game_state}", level="DEBUG", tag="reflex")
        dialogue = game_state.get("dialogue_text") or ""
        mode = game_state.get("mode")
        if mode is None:
            if not self._warned_missing_mode:
                log("Missing mode; defaulted", level="WARN", tag="reflex")
                self._warned_missing_mode = True
            mode = self.default_mode

        action: Optional[Action] = None
        if dialogue:
            action = Action.A
        elif mode == "idle":
            if self.DIRECTIONS:
                action = random.choice(self.DIRECTIONS)
            else:
                log("No directions available", level="WARN", tag="reflex")
        else:
            action = None

        elapsed = (time.perf_counter() - start) * 1000.0
        self._frames += 1
        self._total_latency += elapsed

        log(f"Proposing: {action}", tag="reflex")
        log(f"Decision latency: {elapsed:.3f}ms", level="DEBUG", tag="reflex")
        if self._frames % 100 == 0:
            avg = self._total_latency / self._frames
            log(f"Average reflex latency: {avg:.3f}ms", tag="reflex")

        return action
