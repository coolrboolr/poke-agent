from src.memory.core import ContextMemory
from src.memory.long_term import LongTermMemory
from src.memory.scratchpad import WorkingMemory
from src.memory.short_term import ShortTermMemory


def test_context_update_and_query(tmp_path):
    ltm = LongTermMemory(persist_directory=tmp_path)
    cm = ContextMemory()
    cm.ltm = ltm
    cm.stm = ShortTermMemory()
    cm.scratch = WorkingMemory(ltm, store_path=tmp_path/'obj.json')
    cm.update({'location_id': 1, 'fact': 'Met Oak'})
    facts = cm.query_context('Oak')
    assert any('Oak' in f for f in facts)
