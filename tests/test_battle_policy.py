from src.lanes.tactical.battle_policy import choose_battle_move
from src.utils.actions import Action


def test_effective_move():
    data = {
        "player_hp": 80,
        "player_hp_max": 100,
        "opponent_type": "Fire",
        "moves": [
            {"name": "Tackle", "power": 35, "type": "Normal"},
            {"name": "Water Gun", "power": 40, "type": "Water"},
        ],
    }
    assert choose_battle_move(data) == Action.MOVE_2


def test_fallback_strongest():
    data = {
        "player_hp": 50,
        "player_hp_max": 100,
        "moves": [
            {"name": "Tackle", "power": 35, "type": "Normal"},
            {"name": "Quick Attack", "power": 40, "type": "Normal"},
        ],
    }
    assert choose_battle_move(data) == Action.MOVE_2


def test_no_moves(capsys):
    data = {"moves": []}
    result = choose_battle_move(data)
    captured = capsys.readouterr()
    assert result is None
    assert "No moves available" in captured.out


def test_unreadable_hp():
    data = {
        "player_hp": 10,
        "player_hp_max": 0,
        "opponent_type": "Fire",
        "moves": [
            {"name": "Scratch", "power": 40, "type": "Normal"},
        ],
    }
    assert choose_battle_move(data) == Action.MOVE_1
