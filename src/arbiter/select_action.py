from __future__ import annotations

from typing import Optional

from src.memory import GameState, ContextMemory
from src.lanes.reflex import ReflexAgent
from src.lanes.tactical import TacticalAgent
from src.utils.actions import Action
from src.utils.logger import log

_reflex_agent = ReflexAgent()
_tactical_agent = TacticalAgent()


def get_reflex_action(game_state: GameState) -> Optional[Action]:
    """Return reflex lane's proposed action."""
    action = _reflex_agent.propose_action(game_state)
    log(f"Reflex proposes: {action}", tag="arbiter")
    return action


def get_tactical_action(game_state: GameState, context: ContextMemory) -> Optional[Action]:
    """Return tactical lane's proposed action."""
    action = _tactical_agent.propose_action(game_state, context)
    log(f"Tactical proposes: {action}", tag="arbiter")
    return action


def select_action(game_state: GameState, context: ContextMemory) -> Optional[Action]:
    """Return final action after applying lane priority."""
    action = get_reflex_action(game_state)
    if action is None:
        action = get_tactical_action(game_state, context)
    return action

