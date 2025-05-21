import json
import types
import os
from pathlib import Path

import src.main as main_module
from src.utils.actions import Action


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
    monkeypatch.setattr(main_module, "select_action", lambda state, ctx: None)
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
    monkeypatch.setattr(main_module, "select_action", lambda state, ctx: None)
    monkeypatch.chdir(tmp_path)
    main_module.run_loop(duration_s=1)
    data = json.loads((tmp_path / "logs" / "loop_metrics.json").read_text())
    assert data["average_fps"] < 5


def test_stream_config_load(tmp_path, monkeypatch, capsys):
    env_path = tmp_path / ".env"
    env_path.write_text("PROFILE=dev\nLOOP_DURATION=1\nROM_PATH=test.gba\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(main_module, "EmulatorAdapter", DummyAdapter)
    monkeypatch.setattr(main_module, "FrameBus", DummyBus)
    monkeypatch.setattr(main_module.subprocess, "Popen", lambda *a, **k: None)

    def _load():
        for l in open(".env"):
            if "=" in l:
                k, v = l.strip().split("=", 1)
                os.environ[k] = v

    monkeypatch.setattr(main_module, "load_dotenv", _load)
    monkeypatch.setattr(main_module, "run_loop", lambda duration_s=1: None)
    monkeypatch.setattr(main_module, "select_action", lambda s, c: None)
    main_module.main()
    out = capsys.readouterr().out
    assert "Dev profile enabled" in out
    assert os.getenv("LOOP_DURATION") == "1"


def test_latency_benchmark(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(main_module, "EmulatorAdapter", DummyAdapter)
    monkeypatch.setattr(main_module, "FrameBus", DummyBus)
    monkeypatch.setattr(main_module, "select_action", lambda s, c: None)
    monkeypatch.chdir(tmp_path)
    main_module.run_loop(duration_s=1)
    text = capsys.readouterr().out
    assert "Loop complete FPS" in text


def test_overlay_output(tmp_path, monkeypatch):
    monkeypatch.setattr(main_module, "EmulatorAdapter", DummyAdapter)
    monkeypatch.setattr(main_module, "FrameBus", DummyBus)
    monkeypatch.setattr(main_module, "select_action", lambda s, c: Action.A)
    monkeypatch.chdir(tmp_path)
    main_module.run_loop(duration_s=1)
    data = json.loads(Path("overlay.json").read_text())
    assert data["mode"] == "idle"
    assert data["action"] == "A"

