from src.arbiter.select_action import (
    select_action,
    _reflex_agent,
    _tactical_agent,
    _strategic_agent,
)
from src.memory.core import ContextMemory
from src.utils.actions import Action


def test_reflex_priority(monkeypatch):
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: Action.A)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: Action.LEFT)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.RIGHT)
    ctx = ContextMemory()
    action = select_action({}, ctx)
    assert action == Action.A


def test_tactical_overrides(monkeypatch):
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: None)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: Action.UP)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.DOWN)
    ctx = ContextMemory()
    action = select_action({}, ctx)
    assert action == Action.UP


def test_all_none(monkeypatch, caplog):
    caplog.set_level("INFO")
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: None)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: None)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: None)
    ctx = ContextMemory()
    action = select_action({}, ctx)
    assert action is None
    assert "No action proposed" in caplog.text


def test_log_format(monkeypatch, caplog):
    caplog.set_level("INFO")
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: Action.B)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: None)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.RIGHT)
    ctx = ContextMemory()
    action = select_action({}, ctx)
    assert action == Action.B
    assert "Reflex:" in caplog.text and "Strategic:" in caplog.text and "Selected" in caplog.text


def test_arbiter_priority(monkeypatch):
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: Action.A)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: Action.LEFT)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.RIGHT)
    ctx = ContextMemory()
    assert select_action({}, ctx) == Action.A


def test_arbiter_fallback(monkeypatch):
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: None)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: Action.UP)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.DOWN)
    ctx = ContextMemory()
    assert select_action({}, ctx) == Action.UP


def test_arbiter_no_action(monkeypatch):
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: None)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: None)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: None)
    ctx = ContextMemory()
    assert select_action({}, ctx) is None


def test_arbiter_logs_all(monkeypatch, caplog):
    caplog.set_level("INFO")
    monkeypatch.setattr(_reflex_agent, "propose_action", lambda gs: Action.B)
    monkeypatch.setattr(_tactical_agent, "propose_action", lambda gs, ctx: Action.LEFT)
    monkeypatch.setattr(_strategic_agent, "propose_action", lambda gs, ctx: Action.RIGHT)
    ctx = ContextMemory()
    select_action({}, ctx)
    text = caplog.text
    assert "Reflex proposes" in text
    assert "Tactical proposes" in text
    assert "Strategic proposes" in text
    assert "Selected" in text
