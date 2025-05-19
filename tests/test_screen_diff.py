import numpy as np
from src.perception.screen_diff import ScreenDiffer


def test_screen_diff_changed_and_unchanged():
    differ = ScreenDiffer()
    frame1 = np.zeros((10, 10, 3), dtype=np.uint8)
    assert differ.has_changed(frame1) is False
    frame2 = frame1.copy()
    frame2[0, 0, 0] = 10
    assert differ.has_changed(frame2) is True
    assert differ.has_changed(frame2) is False
