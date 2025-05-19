from pathlib import Path
import cv2
import numpy as np

ASSETS_DIR = Path(__file__).parent / 'assets'


def load_image(name: str) -> np.ndarray:
    path = ASSETS_DIR / name
    frame = cv2.imread(str(path), cv2.IMREAD_COLOR)
    assert frame is not None, f'failed to load {path}'
    return frame
