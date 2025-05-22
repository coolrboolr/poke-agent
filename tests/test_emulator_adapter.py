import os
import types
import time
from src.array_utils import zeros, shape

import src.emulator.adapter as adapter_module
from src.emulator.adapter import EmulatorAdapter


class DummyPopen:
    def __init__(self, *args, **kwargs):
        pass

    def terminate(self):
        pass

    def wait(self):
        pass


def test_read_frame(monkeypatch):
    dummy_image = zeros((5, 5, 3))

    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(Popen=DummyPopen),
    )
    monkeypatch.setattr(adapter_module.ImageGrab, "grab", lambda: dummy_image)

    prev_gui = os.environ.get("ENABLE_GUI")
    prev_display = os.environ.get("DISPLAY")
    os.environ["ENABLE_GUI"] = "true"
    os.environ["DISPLAY"] = ":1"
    emu = EmulatorAdapter(rom_path="test.gba")
    frame = emu.read_frame()
    if prev_gui is None:
        os.environ.pop("ENABLE_GUI", None)
    else:
        os.environ["ENABLE_GUI"] = prev_gui
    if prev_display is None:
        os.environ.pop("DISPLAY", None)
    else:
        os.environ["DISPLAY"] = prev_display
    assert shape(frame) == (5, 5, 3)


def test_send_input_logs(monkeypatch):
    pressed = []
    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(
            Popen=DummyPopen,
            run=lambda args, check=False: pressed.append(args[2]),
        ),
    )
    monkeypatch.setattr(
        adapter_module.ImageGrab,
        "grab",
        lambda: zeros((1, 1, 3)),
    )

    prev = os.environ.get("DISPLAY")
    prev_gui = os.environ.get("ENABLE_GUI")
    os.environ["DISPLAY"] = ":1"
    os.environ["ENABLE_GUI"] = "true"
    emu = EmulatorAdapter(rom_path="test.gba")
    emu.send_input("A")
    assert pressed == ["A"]
    if prev is None:
        os.environ.pop("DISPLAY", None)
    else:
        os.environ["DISPLAY"] = prev
    if prev_gui is None:
        os.environ.pop("ENABLE_GUI", None)
    else:
        os.environ["ENABLE_GUI"] = prev_gui


def test_input_debounce(monkeypatch):
    calls = []
    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(
            Popen=DummyPopen, run=lambda args, check=False: calls.append(time.monotonic())
        ),
    )
    monkeypatch.setattr(
        adapter_module.ImageGrab, "grab", lambda: zeros((1, 1, 3))
    )

    prev = os.environ.get("DISPLAY")
    prev_gui = os.environ.get("ENABLE_GUI")
    os.environ["DISPLAY"] = ":1"
    os.environ["ENABLE_GUI"] = "true"
    emu = EmulatorAdapter(rom_path="test.gba", debounce_interval_ms=80)
    emu.send_input("A")
    emu.send_input("A")
    assert len(calls) == 1
    if prev is None:
        os.environ.pop("DISPLAY", None)
    else:
        os.environ["DISPLAY"] = prev
    if prev_gui is None:
        os.environ.pop("ENABLE_GUI", None)
    else:
        os.environ["ENABLE_GUI"] = prev_gui


def test_send_input_no_display(monkeypatch, capsys):
    pressed = []
    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(
            Popen=DummyPopen, run=lambda args, check=False: pressed.append(args[2])
        ),
    )
    monkeypatch.setattr(adapter_module.ImageGrab, "grab", lambda: zeros((1, 1, 3)))
    prev = os.environ.pop("DISPLAY", None)
    prev_gui = os.environ.get("ENABLE_GUI")
    os.environ["ENABLE_GUI"] = "true"
    emu = EmulatorAdapter(rom_path="test.gba")
    capsys.readouterr()
    emu.send_input("A")
    out = capsys.readouterr().out
    assert "no display" in out
    assert pressed == []
    if prev is not None:
        os.environ["DISPLAY"] = prev
    if prev_gui is None:
        os.environ.pop("ENABLE_GUI", None)
    else:
        os.environ["ENABLE_GUI"] = prev_gui


def test_missing_mgba(monkeypatch, capsys):
    def raise_popen(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(Popen=raise_popen, run=lambda *a, **k: None),
    )
    monkeypatch.setattr(adapter_module.ImageGrab, "grab", lambda: zeros((1, 1, 3)))
    prev_gui = os.environ.get("ENABLE_GUI")
    prev_display = os.environ.get("DISPLAY")
    os.environ["ENABLE_GUI"] = "true"
    os.environ["DISPLAY"] = ":1"
    emu = EmulatorAdapter(rom_path="test.gba")
    if prev_gui is None:
        os.environ.pop("ENABLE_GUI", None)
    else:
        os.environ["ENABLE_GUI"] = prev_gui
    if prev_display is None:
        os.environ.pop("DISPLAY", None)
    else:
        os.environ["DISPLAY"] = prev_display
    out = capsys.readouterr().out
    assert "mGBA not bundled" in out
    assert emu.process is None

