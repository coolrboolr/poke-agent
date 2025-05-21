from src.arbiter.select_action import _reflex_agent, _tactical_agent, _strategic_agent, select_action
from src.lanes.reflex.policy import ReflexAgent
from src.lanes.tactical.agent import TacticalAgent
from src.lanes.strategic.agent import StrategicAgent
from src.memory.core import ContextMemory
from src.utils.actions import Action


def test_integration_loop(monkeypatch):
    reflex = ReflexAgent()
    tactical = TacticalAgent()
    strategic = StrategicAgent()
    monkeypatch.setattr(_reflex_agent, 'propose_action', reflex.propose_action)
    monkeypatch.setattr(_tactical_agent, 'propose_action', tactical.propose_action)
    monkeypatch.setattr(_strategic_agent, 'propose_action', strategic.propose_action)

    ctx = ContextMemory()
    ctx.scratch.add_objective('Reach Pewter City')
    state = {
        'dialogue_text': 'Hi',
        'mode': 'battle',
        'battle_data': {
            'player_hp': 5,
            'player_hp_max': 100,
            'opponent_type': 'Fire',
            'moves': [{'name': 'Tackle', 'power': 35, 'type': 'Normal'}],
        },
        'location': 'Route 1',
    }

    r_action = reflex.propose_action(state)
    t_action = tactical.propose_action(state, ctx)
    s_action = strategic.propose_action(state, ctx)
    final = select_action(state, ctx)

    assert r_action == Action.A
    assert t_action == Action.USE_POTION
    assert s_action == Action.UP
    assert final == Action.A
