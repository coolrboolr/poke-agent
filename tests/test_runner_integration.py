from src.array_utils import zeros, copy_array
import json
from pathlib import Path
from src.perception.runner import PerceptionRunner


def test_runner_integration(tmp_path, monkeypatch, caplog):
    monkeypatch.chdir(tmp_path)
    from src.utils import event_log as el
    el._last_time = 0.0
    caplog.set_level('INFO')
    runner = PerceptionRunner()
    frame1 = zeros((144, 160, 3))
    frame2 = copy_array(frame1)
    frame2[0][0][0] = 255
    state1 = runner.process_frame(frame1)
    state2 = runner.process_frame(frame2)
    assert state1['changed'] is False
    assert state2['changed'] is True
    log_files = list(Path('logs').glob('game_state_*.json'))
    assert log_files
    data = json.loads(log_files[-1].read_text())
    assert 'hp' in data and 'sprites' in data
    assert any('perception' in m for m in caplog.text.splitlines())

