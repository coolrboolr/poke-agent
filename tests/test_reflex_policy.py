from src.lanes.reflex.policy import ReflexAgent
from src.utils.actions import Action


def test_dialogue_trigger():
    agent = ReflexAgent()
    state = {"dialogue_text": "Hello", "mode": "idle"}
    assert agent.propose_action(state) == Action.A


def test_idle_trigger():
    agent = ReflexAgent()
    state = {"dialogue_text": "", "mode": "idle"}
    action = agent.propose_action(state)
    assert action in {Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN}


def test_noop_conditions():
    agent = ReflexAgent()
    for mode in ["battle", "cutscene"]:
        state = {"dialogue_text": "", "mode": mode}
        assert agent.propose_action(state) is None

