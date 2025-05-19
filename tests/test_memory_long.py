from src.memory.long_term import LongTermMemory


def test_ltm_add_query(tmp_path):
    ltm = LongTermMemory(persist_directory=tmp_path)
    ltm.add_fact("Caught Pikachu near Viridian Forest", {"location": "viridian"})
    ltm.add_fact("Defeated Brock in Pewter Gym", {"location": "pewter"})

    results = ltm.query("Where was Pikachu caught?")
    assert any("Pikachu" in r for r in results)
