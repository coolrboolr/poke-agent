from pathlib import Path
from src.array_utils import zeros, fill_rect

ASSETS_DIR = Path(__file__).parent / 'assets'


def load_image(name: str):
    """Return stub frames used for tests."""
    if name == "blank.png":
        return zeros((144, 160, 3))
    if name == "battle.png":
        frame = zeros((144, 160, 3))
        # full player bar
        fill_rect(frame, 10, 120, 70, 124, (0, 200, 0))
        # half enemy bar
        fill_rect(frame, 90, 20, 120, 24, (0, 200, 0))
        return frame
    if name == "textbox.png":
        return zeros((144, 160, 3))
    raise FileNotFoundError(name)
