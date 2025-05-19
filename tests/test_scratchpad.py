from src.memory.long_term import LongTermMemory
from src.memory.scratchpad import WorkingMemory


def test_objective_flow(tmp_path):
    ltm = LongTermMemory(persist_directory=tmp_path)
    path = tmp_path / "obj.json"
    wm = WorkingMemory(ltm, store_path=path)

    wm.add_objective("Catch Pikachu")
    wm.add_objective("Beat Brock")
    assert wm.get_objectives() == ["Catch Pikachu", "Beat Brock"]

    wm.complete_objective(0)
    assert wm.get_objectives() == ["Beat Brock"]

    ltm.add_fact("Caught Pikachu near Viridian Forest", {"location": "viridian"})
    facts = wm.top_n_relevant_facts()
    assert any("Pikachu" in f for f in facts)

    # persistence check
    wm2 = WorkingMemory(ltm, store_path=path)
    assert wm2.get_objectives() == ["Beat Brock"]
