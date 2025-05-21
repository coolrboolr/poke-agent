from __future__ import annotations

import time
from typing import Optional

from src.memory import GameState, ContextMemory
from src.utils.actions import Action
from src.utils.logger import log


class StrategicAgent:
    """Long-term planner using high-level objectives."""

    def __init__(self) -> None:
        self._frames = 0
        self._total_latency = 0.0

    def _current_goal(self, memory: ContextMemory) -> Optional[str]:
        """Return the first active objective description if any."""
        goals = memory.scratch.get_objectives()
        return goals[0] if goals else None

    def propose_action(self, game_state: GameState, memory: ContextMemory) -> Optional[Action]:
        """Suggest an action toward completing the current strategic objective."""
        start = time.perf_counter()
        goal = self._current_goal(memory)
        location = game_state.get("location")

        action: Optional[Action] = None

        # Very simple heuristic rules for demo purposes
        if goal and "pewter" in goal.lower():
            if location and location.lower().startswith("pewter"):
                action = None  # Goal reached
            else:
                # Assume Pewter City is to the north of current position
                action = Action.UP

        elapsed = (time.perf_counter() - start) * 1000.0
        self._frames += 1
        self._total_latency += elapsed
        log(f"Proposing: {action}", tag="strategic")
        log(f"Decision latency: {elapsed:.3f}ms", level="DEBUG", tag="strategic")
        if self._frames % 100 == 0:
            avg = self._total_latency / self._frames
            log(f"Average strategic latency: {avg:.3f}ms", tag="strategic")
        return action
