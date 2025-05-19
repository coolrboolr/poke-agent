from src.array_utils import zeros
from src.perception.sprite_detector import SpriteDetector


def test_sprite_detector_returns_player():
    frame = zeros((10, 10, 3))
    det = SpriteDetector()
    boxes = det.detect(frame)
    assert isinstance(boxes, list)
    assert boxes and boxes[0]['name'] == 'player'

