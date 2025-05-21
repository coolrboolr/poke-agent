from __future__ import annotations

from src.memory.short_term import GameState
from src.game_profiles.registry import load_profile


def compute_reward(prev_state: GameState, curr_state: GameState) -> float:
    """Delegate reward computation to the active GameProfile."""
    profile = load_profile()
    return profile.get_reward(prev_state, curr_state)
