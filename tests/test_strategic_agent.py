from src.lanes.strategic.agent import StrategicAgent
from src.memory.core import ContextMemory
from src.memory.long_term import LongTermMemory
from src.memory.scratchpad import WorkingMemory
from src.utils.actions import Action


def _context(tmp_path) -> ContextMemory:
    ltm = LongTermMemory(persist_directory=tmp_path)
    ctx = ContextMemory()
    ctx.ltm = ltm
    ctx.scratch = WorkingMemory(ltm, store_path=tmp_path / "obj.json")
    return ctx


def test_head_to_pewter(tmp_path):
    ctx = _context(tmp_path)
    ctx.scratch.add_objective("head to Pewter")
    agent = StrategicAgent()
    state = {"location": "Viridian"}
    action = agent.propose_action(state, ctx)
    assert action == Action.UP


def test_at_destination(tmp_path):
    ctx = _context(tmp_path)
    ctx.scratch.add_objective("head to Pewter")
    agent = StrategicAgent()
    state = {"location": "Pewter City"}
    assert agent.propose_action(state, ctx) is None


def test_strategic_goal_selection(tmp_path):
    ctx = _context(tmp_path)
    ctx.scratch.add_objective("Reach Pewter City")
    agent = StrategicAgent()
    state = {"location": "Route 2"}
    assert agent.propose_action(state, ctx) == Action.UP


def test_goal_completion_fallback(tmp_path):
    ctx = _context(tmp_path)
    ctx.scratch.add_objective("Reach Pewter City")
    agent = StrategicAgent()
    state = {"location": "Pewter City"}
    assert agent.propose_action(state, ctx) is None


def test_strategic_noop(tmp_path):
    ctx = _context(tmp_path)
    agent = StrategicAgent()
    state = {"location": "Viridian"}
    assert agent.propose_action(state, ctx) is None
