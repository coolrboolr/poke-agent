import numpy as np
from PIL import Image
import types

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
    dummy_image = Image.new("RGB", (5, 5), color="red")

    monkeypatch.setattr(
        adapter_module,
        "subprocess",
        types.SimpleNamespace(Popen=DummyPopen),
    )
    monkeypatch.setattr(adapter_module.ImageGrab, "grab", lambda: dummy_image)

    emu = EmulatorAdapter(rom_path="test.gba")
    frame = emu.read_frame()
    assert isinstance(frame, np.ndarray)
    assert frame.shape == (5, 5, 3)


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
        lambda: Image.new("RGB", (1, 1)),
    )

    emu = EmulatorAdapter(rom_path="test.gba")
    emu.send_input("A")
    assert pressed == ["A"]
