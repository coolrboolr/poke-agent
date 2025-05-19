import os
import subprocess
from typing import Optional
import time

import numpy as np
from PIL import ImageGrab


from src.utils.logger import log


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

    def read_frame(self) -> np.ndarray:
        """Capture the current screen frame as a NumPy array."""
        img = ImageGrab.grab()
        frame = np.array(img)
        log(f"Frame captured: {frame.shape}", tag="emulator")
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
