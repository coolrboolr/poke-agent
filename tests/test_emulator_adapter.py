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

    emu = EmulatorAdapter(rom_path="test.gba")
    frame = emu.read_frame()
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

    emu = EmulatorAdapter(rom_path="test.gba")
    emu.send_input("A")
    assert pressed == ["A"]


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

    emu = EmulatorAdapter(rom_path="test.gba", debounce_interval_ms=80)
    emu.send_input("A")
    emu.send_input("A")
    assert len(calls) == 1

