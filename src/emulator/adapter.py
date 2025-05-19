import os
import subprocess
from typing import Optional

import numpy as np
from PIL import ImageGrab


from src.utils.logger import log


class EmulatorAdapter:
    """Launch mGBA and interact via screenshots and keypresses."""

    def __init__(self, rom_path: Optional[str] = None) -> None:
        self.rom_path = rom_path or os.getenv("ROM_PATH")
        if not self.rom_path:
            raise FileNotFoundError("ROM_PATH is not set")

        self.process: Optional[subprocess.Popen] = None
        self._launch_emulator()

    def _launch_emulator(self) -> None:
        cmd = ["mgba-sdl", self.rom_path]
        try:
            self.process = subprocess.Popen(cmd)
            log("mGBA launched")
        except FileNotFoundError:
            log(
                "mGBA executable not found; continuing without emulator",
                level="WARNING",
            )
            self.process = None

    def read_frame(self) -> np.ndarray:
        """Capture the current screen frame as a NumPy array."""
        img = ImageGrab.grab()
        frame = np.array(img)
        return frame

    def send_input(self, button: str) -> None:
        """Inject a keypress into the emulator using xdotool."""
        subprocess.run(["xdotool", "key", button], check=False)
        log(f"Input sent: {button}")

    def close(self) -> None:
        if self.process:
            self.process.terminate()
            self.process.wait()
