from __future__ import annotations

from typing import Optional

from src.memory import GameState, ContextMemory
from src.lanes.reflex import ReflexAgent
from src.lanes.tactical import TacticalAgent
from src.lanes.strategic import StrategicAgent
from src.utils.actions import Action
from src.utils.logger import log

_last_brain_state = {
    "reflex": None,
    "tactical": None,
    "strategic": None,
    "selected": None,
}

_reflex_agent = ReflexAgent()
_tactical_agent = TacticalAgent()
_strategic_agent = StrategicAgent()


def get_last_brain_state() -> dict:
    """Return the most recently computed brain state."""
    return _last_brain_state.copy()


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


def get_strategic_action(game_state: GameState, context: ContextMemory) -> Optional[Action]:
    """Return strategic lane's proposed action."""
    action = _strategic_agent.propose_action(game_state, context)
    log(f"Strategic proposes: {action}", tag="arbiter")
    return action


def select_action(game_state: GameState, context: ContextMemory) -> Optional[Action]:
    """Return final action after applying lane priority."""
    reflex = get_reflex_action(game_state)
    tactical = get_tactical_action(game_state, context)
    strategic = get_strategic_action(game_state, context)

    selected = None
    if reflex is not None:
        selected = reflex
        source = "Reflex"
    elif tactical is not None:
        selected = tactical
        source = "Tactical"
    elif strategic is not None:
        selected = strategic
        source = "Strategic"
    else:
        source = None

    if selected is not None:
        log(
            f"Reflex: {reflex} | Tactical: {tactical} | Strategic: {strategic} → Selected: {selected}",
            tag="arbiter",
        )
    else:
        log("No action proposed", tag="arbiter")

    _last_brain_state.update(
        {
            "reflex": reflex.name if isinstance(reflex, Action) else None,
            "tactical": tactical.name if isinstance(tactical, Action) else None,
            "strategic": strategic.name if isinstance(strategic, Action) else None,
            "selected": selected.name if isinstance(selected, Action) else None,
        }
    )

    return selected

