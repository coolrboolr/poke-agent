import json
from pathlib import Path

from src.memory.long_term import LongTermMemory
from src.memory.scratchpad import WorkingMemory


def dump_context(memory_dir: str = "memory_store", logs_dir: str = "logs") -> None:
    ltm = LongTermMemory(persist_directory=memory_dir)
    wm = WorkingMemory(ltm)
    stm_files = sorted(Path(logs_dir).glob("game_state_*.json"))[-5:]
    states = [json.loads(Path(p).read_text()) for p in stm_files]

    print("Last 3 facts:")
    for f in ltm.last_facts(3):
        print("-", f)

    print("Current objectives:")
    for obj in wm.get_objectives():
        print("-", obj)

    print("Last 5 GameStates:")
    for s in states:
        print(s)


def main() -> None:
    dump_context()


if __name__ == "__main__":
    main()
