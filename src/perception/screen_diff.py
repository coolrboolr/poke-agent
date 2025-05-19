import numpy as np
from src.utils.logger import log


class ScreenDiffer:
    """Detect screen changes via pixel sum delta."""

    def __init__(self, threshold: int = 1000) -> None:
        self.prev_hash: int | None = None
        self.threshold = threshold

    def has_changed(self, curr_frame: np.ndarray) -> bool:
        """Return True if frame changed beyond threshold."""
        curr_hash = int(curr_frame.sum())
        if self.prev_hash is None:
            self.prev_hash = curr_hash
            return False
        delta = abs(curr_hash - self.prev_hash)
        self.prev_hash = curr_hash
        changed = delta > self.threshold
        log(f"Screen changed={changed} delta={delta}", tag="perception")
        return changed
