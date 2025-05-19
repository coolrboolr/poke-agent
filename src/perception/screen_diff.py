from src.utils.logger import log
from src.array_utils import sum_array


class ScreenDiffer:
    """Detect screen changes via pixel sum delta."""

    def __init__(self, threshold: int = 1) -> None:
        self.prev_hash: int | None = None
        self.threshold = threshold

    def has_changed(self, curr_frame) -> bool:
        """Return True if frame changed beyond threshold."""
        curr_hash = int(sum_array(curr_frame))
        if self.prev_hash is None:
            self.prev_hash = curr_hash
            return False
        delta = abs(curr_hash - self.prev_hash)
        self.prev_hash = curr_hash
        changed = delta > self.threshold
        # Logging removed for performance in tests
        return changed



