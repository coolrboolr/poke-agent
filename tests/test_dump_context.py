import json
from pathlib import Path
from src.memory.long_term import LongTermMemory
from src.memory.scratchpad import WorkingMemory
from src.utils.event_log import log_game_state
import tools.dump_context as dump


def test_dump_context_output(tmp_path, capsys):
    mem_dir = tmp_path / "mem"
    log_dir = tmp_path / "logs"
    from src.utils import event_log as el
    el._last_time = 0.0
    ltm = LongTermMemory(persist_directory=mem_dir)
    wm = WorkingMemory(ltm, store_path=mem_dir / "obj.json")
    wm.add_objective("Find Oak")
    ltm.add_fact("Met Oak", {})
    log_game_state({"loc": 1}, log_dir=log_dir)
    import time as _t
    _t.sleep(1.1)
    log_game_state({"loc": 2}, log_dir=log_dir)
    dump.dump_context(memory_dir=mem_dir, logs_dir=log_dir)
    out = capsys.readouterr().out
    assert "Met Oak" in out
    assert "Find Oak" in out
