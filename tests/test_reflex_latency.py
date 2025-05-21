import time

from src.lanes.reflex.policy import ReflexAgent


def test_reflex_latency():
    agent = ReflexAgent()
    state = {"dialogue_text": "", "mode": "idle"}
    times = []
    for _ in range(50):
        t0 = time.perf_counter()
        agent.propose_action(state)
        times.append(time.perf_counter() - t0)
    avg_ms = sum(times) / len(times) * 1000
    assert avg_ms < 2.0

