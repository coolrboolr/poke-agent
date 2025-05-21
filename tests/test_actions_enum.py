from src.utils.actions import Action


def test_enum_values():
    assert Action.A.value == "A"
    assert Action.LEFT.value == "LEFT"
    assert Action.RIGHT.value == "RIGHT"
    assert Action.UP.value == "UP"
    assert Action.DOWN.value == "DOWN"
    assert Action.START.value == "START"

