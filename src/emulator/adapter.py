import os
import subprocess
from typing import Optional
import time

from src.array_utils import zeros, shape

try:
    from PIL import ImageGrab  # type: ignore
except Exception:  # pragma: no cover - fallback when Pillow not installed
    class ImageGrab:
        @staticmethod
        def grab():
            raise RuntimeError("ImageGrab.grab unavailable")

from src.utils.logger import log

DUMMY_FRAME = zeros((144, 160, 3))


class EmulatorAdapter:
    """Launch mGBA and interact via screenshots and keypresses."""

    def __init__(self, rom_path: Optional[str] = None, debounce_interval_ms: int = 80) -> None:
        self.rom_path = rom_path or os.getenv("ROM_PATH")
        if not self.rom_path:
            raise FileNotFoundError("ROM_PATH is not set")

        self.debounce_interval_ms = debounce_interval_ms
        self._last_input_time = 0.0

        self.process: Optional[subprocess.Popen] = None
        self._launch_emulator()

    def _launch_emulator(self) -> None:
        cmd = ["mgba-sdl", self.rom_path]
        try:
            self.process = subprocess.Popen(cmd)
            log("mGBA launched", tag="emulator")
        except FileNotFoundError:
            log(
                "mGBA executable not found; continuing without emulator",
                level="WARN",
                tag="emulator",
            )
            self.process = None

    def read_frame(self):
        """Capture the current screen frame as a nested list array."""
        try:
            img = ImageGrab.grab()
        except Exception as e:  # pragma: no cover - fallback when grab fails
            log(f"Failed to read frame: {e}", level="WARN", tag="emulator")
            frame = zeros((len(DUMMY_FRAME), len(DUMMY_FRAME[0]), 3))
        else:
            if hasattr(img, "size") and hasattr(img, "getdata"):
                w, h = img.size
                data = list(img.getdata())
                frame = [
                    [list(data[y * w + x]) for x in range(w)]
                    for y in range(h)
                ]
            else:
                frame = img  # type: ignore
        log(f"Frame captured: {shape(frame)}", tag="emulator")
        if os.getenv("PROFILE") == "dev":
            assert shape(frame) == (144, 160, 3), f"Bad frame shape: {shape(frame)}"
        return frame

    def send_input(self, button: str) -> None:
        """Inject a keypress into the emulator using xdotool."""
        now = time.monotonic()
        if now - self._last_input_time < self.debounce_interval_ms / 1000.0:
            log(f"Input debounced: {button}", level="WARN", tag="emulator")
            return
        subprocess.run(["xdotool", "key", button], check=False)
        self._last_input_time = now
        log(f"Input sent: {button}", tag="emulator")

    def close(self) -> None:
        if self.process:
            self.process.terminate()
            self.process.wait()
        log("Emulator closed", tag="emulator")
