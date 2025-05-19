import time
from typing import List, Dict

import numpy as np

from src.utils.logger import log


class SpriteDetector:
    """Stub interface for future YOLOv8 detection."""

    def detect(self, frame: np.ndarray) -> List[Dict]:
        start = time.perf_counter()
        time.sleep(0.001)  # simulate inference latency
        boxes = [{"name": "player", "x": 12, "y": 20}]
        elapsed = (time.perf_counter() - start) * 1000
        log(f"Sprite detect {boxes} in {elapsed:.2f}ms", tag="perception")
        return boxes
