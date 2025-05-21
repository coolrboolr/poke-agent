from __future__ import annotations

from typing import Optional

from src.memory import GameState
from src.lanes.reflex import ReflexAgent
from src.utils.actions import Action
from src.utils.logger import log

_reflex_agent = ReflexAgent()


def get_reflex_action(game_state: GameState) -> Optional[Action]:
    """Return reflex lane's proposed action."""
    action = _reflex_agent.propose_action(game_state)
    log(f"Reflex proposes: {action}", tag="arbiter")
    return action

