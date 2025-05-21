from src.lanes.tactical.pathfinder import is_player_stuck
from src.memory.short_term import ShortTermMemory


def test_player_stuck():
    stm = ShortTermMemory(maxlen=5)
    for _ in range(5):
        stm.append({"position": (5, 5)})
    assert is_player_stuck(stm) is True


def test_player_moving():
    stm = ShortTermMemory(maxlen=5)
    stm.append({"position": (5, 5)})
    stm.append({"position": (5, 6)})
    stm.append({"position": (5, 7)})
    assert is_player_stuck(stm) is False
