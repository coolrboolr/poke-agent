from __future__ import annotations

from src.memory.short_term import GameState
from src.utils.logger import log


def compute_reward(prev_state: GameState, curr_state: GameState) -> float:
    """Simple reward calculation based on game events."""
    reward = 0.0

    if curr_state.get("badges", 0) > prev_state.get("badges", 0):
        reward += 10.0
        log("Badge gained +10", tag="rl")

    if (
        prev_state.get("in_battle")
        and not curr_state.get("in_battle")
        and curr_state.get("battle_result") == "win"
    ):
        reward += 5.0
        log("Battle win +5", tag="rl")

    if curr_state.get("fainted") or curr_state.get("stuck"):
        reward -= 10.0
        log("Penalty -10", tag="rl")

    return reward
