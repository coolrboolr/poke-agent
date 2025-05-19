from src.array_utils import ones
from src.perception.hud_parser import HUDParser


def fake_frame(player_ratio=1.0, enemy_ratio=1.0):
    frame = ones((144, 160, 3))
    # scale to 255
    for y in range(144):
        for x in range(160):
            frame[y][x] = [255, 255, 255]
    px = (0, 200, 0)
    p_start, p_end = int(60 * player_ratio), 60
    e_start, e_end = int(60 * enemy_ratio), 60
    # player bar region 10..70 x 120..124
    for y in range(120, 124):
        for x in range(10, 10 + p_end):
            if x < 10 + p_start:
                frame[y][x] = px
    # enemy bar region 90..150 x 20..24
    for y in range(20, 24):
        for x in range(90, 90 + e_end):
            if x < 90 + e_start:
                frame[y][x] = px
    return frame


def test_hp_extraction_full_and_empty():
    parser = HUDParser()
    full = fake_frame(1.0, 1.0)
    result = parser.parse(full)
    assert result['player_hp'] == 1.0
    assert result['enemy_hp'] == 1.0

    empty = fake_frame(0.0, 0.0)
    result = parser.parse(empty)
    assert result['player_hp'] == 0.0
    assert result['enemy_hp'] == 0.0

