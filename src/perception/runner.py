from typing import Dict, Any
import numpy as np

from src.utils.event_log import log_game_state
from src.perception.screen_diff import ScreenDiffer
from src.perception.hud_parser import HUDParser
from src.perception.sprite_detector import SpriteDetector


class PerceptionRunner:
    """Orchestrate perception modules into a game state."""

    def __init__(self) -> None:
        self.differ = ScreenDiffer()
        self.hud = HUDParser()
        self.sprites = SpriteDetector()

    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        changed = self.differ.has_changed(frame)
        hud = self.hud.parse(frame)
        sprites = self.sprites.detect(frame)
        state = {
            "changed": changed,
            "dialogue": hud.get("dialogue_text", ""),
            "hp": {
                "player": hud.get("player_hp", 0.0),
                "enemy": hud.get("enemy_hp", 0.0),
            },
            "sprites": sprites,
        }
        log_game_state(state)
        return state
