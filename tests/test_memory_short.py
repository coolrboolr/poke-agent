from src.memory.short_term import ShortTermMemory


def test_stm_buffer_and_transitions(capsys):
    stm = ShortTermMemory(maxlen=3)
    f1 = {"location_id": 1, "mode": "map"}
    f2 = {"location_id": 1, "mode": "map"}
    f3 = {"location_id": 2, "mode": "battle"}

    stm.append(f1)
    stm.append(f2)
    stm.append(f3)

    assert len(stm.buffer) == 3
    assert stm.get_last(2) == [f2, f3]

    captured = capsys.readouterr()
    assert "Scene transition" in captured.out
