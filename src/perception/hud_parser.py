import pytesseract

from src.utils.logger import log


class HUDParser:
    """Parse HUD elements like dialogue text and HP bars."""

    # Box coordinates (x1, y1, x2, y2) for sample 160x144 images
    TEXTBOX_REGION = (0, 110, 160, 144)
    PLAYER_HP_BAR = (10, 120, 70, 124)
    ENEMY_HP_BAR = (90, 20, 150, 24)

    def _extract_text(self, frame) -> str:
        x1, y1, x2, y2 = self.TEXTBOX_REGION
        crop = [row[x1:x2] for row in frame[y1:y2]]
        try:
            text = pytesseract.image_to_string(crop)
            log(f"OCR raw output: {text}", level="DEBUG", tag="perception")
        except Exception as e:
            log(f"OCR failed: {e}", level="WARN", tag="perception")
            text = ""
        cleaned = text.replace("\n", " ").strip()
        cleaned = cleaned.replace("0HP", "OHP")  # example typo fix
        return cleaned

    def _hp_from_region(self, frame, box) -> float:
        x1, y1, x2, y2 = box
        width = x2 - x1
        if width <= 0:
            return 0.0
        filled = 0
        for x in range(x1, x2):
            for y in range(y1, y2):
                r, g, b = frame[y][x]
                if g > 150 and r < 120 and b < 120:
                    filled += 1
                    break
        return filled / width

    def parse(self, frame) -> dict:
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
