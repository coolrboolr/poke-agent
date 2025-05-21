from __future__ import annotations

from typing import Dict, List, Optional

from src.utils.actions import Action
from src.utils.logger import log

# Very small type chart for demonstration
_TYPE_CHART = {
    ("Water", "Fire"): 2.0,
    ("Fire", "Water"): 0.5,
    ("Grass", "Water"): 2.0,
    ("Water", "Grass"): 0.5,
}

_MOVE_ACTIONS = [Action.MOVE_1, Action.MOVE_2, Action.MOVE_3, Action.MOVE_4]


def _effectiveness(move_type: str, target_type: Optional[str]) -> float:
    if target_type is None:
        return 1.0
    return _TYPE_CHART.get((move_type, target_type), 1.0)


def choose_battle_move(battle_data: Dict) -> Optional[Action]:
    """Return best Action for the current battle state."""
    moves: List[Dict] = battle_data.get("moves")
    if not moves:
        log("No moves available", level="WARN", tag="tactical")
        return None

    hp = battle_data.get("player_hp")
    max_hp = battle_data.get("player_hp_max")
    if hp is not None and max_hp:
        try:
            if hp / max_hp < 0.2:
                log("HP low, using potion", tag="tactical")
                return Action.USE_POTION
        except ZeroDivisionError:
            log("HP bar unreadable", level="WARN", tag="tactical")

    target_type = battle_data.get("opponent_type")
    best_score = -1.0
    best_idx = 0
    for idx, move in enumerate(moves):
        power = move.get("power", 0)
        mtype = move.get("type")
        eff = _effectiveness(mtype, target_type)
        score = eff * power
        if score > best_score:
            best_score = score
            best_idx = idx
    if best_idx >= len(_MOVE_ACTIONS):
        best_idx = 0
    return _MOVE_ACTIONS[best_idx]
