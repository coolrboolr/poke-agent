from src.lanes.reflex.policy import ReflexAgent
from src.utils.actions import Action


def test_dialogue_triggers_a():
    agent = ReflexAgent()
    state = {"dialogue_text": "Hello", "mode": "idle"}
    assert agent.propose_action(state) == Action.A


def test_idle_random_move():
    agent = ReflexAgent()
    state = {"dialogue_text": "", "mode": "idle"}
    action = agent.propose_action(state)
    assert action in {Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN}


def test_battle_none():
    agent = ReflexAgent()
    state = {"dialogue_text": "", "mode": "battle"}
    assert agent.propose_action(state) is None

