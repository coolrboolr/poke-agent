import numpy as np
import json
from pathlib import Path
from src.perception.runner import PerceptionRunner


def test_runner_integration(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    caplog.set_level('INFO')
    runner = PerceptionRunner()
    frame1 = np.zeros((160, 144, 3), dtype=np.uint8)
    frame2 = frame1.copy()
    frame2[0,0,0] = 255
    state1 = runner.process_frame(frame1)
    state2 = runner.process_frame(frame2)
    assert state1['changed'] is False
    assert state2['changed'] is True
    log_files = list(Path('logs').glob('game_state_*.json'))
    assert log_files
    data = json.loads(log_files[-1].read_text())
    assert 'hp' in data and 'sprites' in data
    assert any('perception' in m for m in caplog.text.splitlines())
