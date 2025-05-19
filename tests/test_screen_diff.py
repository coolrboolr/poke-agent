from src.array_utils import zeros, copy_array
from src.perception.screen_diff import ScreenDiffer


def test_screen_diff_changed_and_unchanged():
    differ = ScreenDiffer()
    frame1 = zeros((10, 10, 3))
    assert differ.has_changed(frame1) is False
    frame2 = copy_array(frame1)
    frame2[0][0][0] = 10
    assert differ.has_changed(frame2) is True
    assert differ.has_changed(frame2) is False

