from src.lanes.tactical.agent import TacticalAgent
from src.memory.core import ContextMemory
from src.utils.actions import Action


def test_battle_best_move():
    agent = TacticalAgent()
    context = ContextMemory()
    state = {
        "mode": "battle",
        "battle_data": {
            "player_hp": 80,
            "player_hp_max": 100,
            "opponent_type": "Fire",
            "moves": [
                {"name": "Tackle", "power": 35, "type": "Normal"},
                {"name": "Water Gun", "power": 40, "type": "Water"},
            ],
        },
    }
    action = agent.propose_action(state, context)
    assert action == Action.MOVE_2


def test_low_hp_potion():
    agent = TacticalAgent()
    context = ContextMemory()
    state = {
        "mode": "battle",
        "battle_data": {
            "player_hp": 10,
            "player_hp_max": 100,
            "opponent_type": "Fire",
            "moves": [
                {"name": "Scratch", "power": 40, "type": "Normal"}
            ],
        },
    }
    assert agent.propose_action(state, context) == Action.USE_POTION


def test_stuck_navigation():
    agent = TacticalAgent()
    context = ContextMemory()
    for _ in range(5):
        context.stm.append({"position": (1, 1), "mode": "map"})
    state = {"mode": "map"}
    action = agent.propose_action(state, context)
    assert action in {Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN}


def test_idle_none():
    agent = TacticalAgent()
    context = ContextMemory()
    context.stm.append({"position": (1, 1), "mode": "map"})
    context.stm.append({"position": (2, 1), "mode": "map"})
    state = {"mode": "map"}
    assert agent.propose_action(state, context) is None
