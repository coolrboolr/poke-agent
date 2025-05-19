import json
import time
from pathlib import Path
from src.utils.event_log import log_game_state, _last_time


def test_log_game_state_throttle(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    from src.utils import event_log as el
    el._last_time = 0.0
    monkeypatch.setattr('time.time', lambda: 1000.0)
    log_game_state({'a': 1})
    monkeypatch.setattr('time.time', lambda: 1000.5)
    log_game_state({'a': 2})
    files = list(Path('logs').glob('game_state_*.json'))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data['a'] == 1
