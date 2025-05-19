import json
import time
from pathlib import Path
from typing import Dict

from src.utils.logger import log

_last_time = 0.0


def log_game_state(state: Dict, log_dir: Path = Path("logs")) -> None:
    """Persist GameState to disk at most once per second."""
    global _last_time
    now = time.time()
    if now - _last_time < 1.0:
        return
    log_dir.mkdir(exist_ok=True)
    path = log_dir / f"game_state_{int(now)}.json"
    with open(path, "w") as f:
        json.dump(state, f)
    log(f"GameState logged to {path}", tag="perception")
    _last_time = now
