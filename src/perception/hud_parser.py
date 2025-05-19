import numpy as np
from PIL import Image
import pytesseract

from src.utils.logger import log


class HUDParser:
    """Parse HUD elements like dialogue text and HP bars."""

    # Box coordinates (x1, y1, x2, y2) for sample 160x144 images
    TEXTBOX_REGION = (0, 110, 160, 144)
    PLAYER_HP_BAR = (10, 120, 70, 124)
    ENEMY_HP_BAR = (90, 20, 150, 24)

    def _extract_text(self, frame: np.ndarray) -> str:
        x1, y1, x2, y2 = self.TEXTBOX_REGION
        crop = frame[y1:y2, x1:x2]
        pil_img = Image.fromarray(crop)
        text = pytesseract.image_to_string(pil_img)
        cleaned = text.replace("\n", " ").strip()
        cleaned = cleaned.replace("0HP", "OHP")  # example typo fix
        return cleaned

    def _hp_from_region(self, frame: np.ndarray, box) -> float:
        x1, y1, x2, y2 = box
        region = frame[y1:y2, x1:x2]
        green = (
            (region[:, :, 1] > 150)
            & (region[:, :, 0] < 120)
            & (region[:, :, 2] < 120)
        )
        cols = green.any(axis=0)
        ratio = cols.mean() if cols.size else 0.0
        return float(ratio)

    def parse(self, frame: np.ndarray) -> dict:
        dialogue = self._extract_text(frame)
        player_hp = self._hp_from_region(frame, self.PLAYER_HP_BAR)
        enemy_hp = self._hp_from_region(frame, self.ENEMY_HP_BAR)
        log(
            f"HUD parsed text='{dialogue}' player_hp={player_hp:.2f} enemy_hp={enemy_hp:.2f}",
            tag="perception",
        )
        return {
            "dialogue_text": dialogue,
            "player_hp": player_hp,
            "enemy_hp": enemy_hp,
        }
