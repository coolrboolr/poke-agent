import json
import types
import os

import src.main as main_module


class DummyAdapter:
    def __init__(self, *args, **kwargs):
        self.read_calls = 0

    def read_frame(self):
        from src.array_utils import zeros
        self.read_calls += 1
        return zeros((144, 160, 3))

    def send_input(self, *args, **kwargs):
        pass

    def close(self):
        pass


class DummyBus:
    def __init__(self, *args, **kwargs):
        self.publish_calls = 0

    def publish(self, frame):
        self.publish_calls += 1

    def close(self):
        pass


def test_loop_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(main_module, "EmulatorAdapter", DummyAdapter)
    monkeypatch.setattr(main_module, "FrameBus", DummyBus)
    logs = tmp_path / "logs"
    monkeypatch.chdir(tmp_path)
    main_module.run_loop(duration_s=1)

    metrics_file = logs / "loop_metrics.json"
    assert metrics_file.exists()
    data = json.loads(metrics_file.read_text())
    assert data["average_fps"] > 0


def test_low_fps_warning(tmp_path, monkeypatch):
    class SlowAdapter(DummyAdapter):
        def read_frame(self):
            from src.array_utils import zeros
            import time as _t
            _t.sleep(0.3)
            return zeros((144, 160, 3))

    monkeypatch.setattr(main_module, "EmulatorAdapter", SlowAdapter)
    monkeypatch.setattr(main_module, "FrameBus", DummyBus)
    monkeypatch.chdir(tmp_path)
    main_module.run_loop(duration_s=1)
    data = json.loads((tmp_path / "logs" / "loop_metrics.json").read_text())
    assert data["average_fps"] < 5

