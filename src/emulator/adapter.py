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


def _env_use_gui() -> bool:
    return os.environ.get("ENABLE_GUI", "true").lower() == "true"


DUMMY_FRAME = zeros((144, 160, 3))


class EmulatorAdapter:
    """Launch mGBA and interact via screenshots and keypresses."""

    def __init__(
        self, rom_path: Optional[str] = None, debounce_interval_ms: int = 80
    ) -> None:
        self.rom_path = rom_path or os.getenv("ROM_PATH")
        if not self.rom_path:
            raise FileNotFoundError("ROM_PATH is not set")

        self.debounce_interval_ms = debounce_interval_ms
        self._last_input_time = 0.0

        self.process: Optional[subprocess.Popen] = None
        self.use_gui = _env_use_gui()
        self._dummy_frames = 0
        self._launch_emulator()

    def _launch_emulator(self) -> None:
        if not self.use_gui:
            log("GUI disabled; running in dummy emulator mode", tag="emulator")
            self.process = None
            return

        cmd = ["mgba-sdl", self.rom_path]
        display = os.getenv("DISPLAY")
        if not display:
            cmd = ["xvfb-run", "-a"] + cmd
        log(f"Launching emulator command: {' '.join(cmd)}", tag="emulator")
        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=getattr(subprocess, "PIPE", None),
                stderr=getattr(subprocess, "PIPE", None),
            )
            log("mGBA launched", tag="emulator")
        except FileNotFoundError:
            log(
                "mGBA not bundled: running in dummy mode",
                level="WARN",
                tag="emulator",
            )
            self.process = None
            self.use_gui = False

    def read_frame(self):
        """Capture the current screen frame as a nested list array."""
        if not self.use_gui or not os.getenv("DISPLAY"):
            log("GUI disabled; returning dummy frame", tag="emulator")
            frame = zeros((len(DUMMY_FRAME), len(DUMMY_FRAME[0]), 3))
            self._dummy_frames += 1
        else:
            try:
                img = ImageGrab.grab()
            except Exception as e:  # pragma: no cover - fallback when grab fails
                log(f"Failed to read frame: {e}", level="WARN", tag="emulator")
                frame = zeros((len(DUMMY_FRAME), len(DUMMY_FRAME[0]), 3))
                self._dummy_frames += 1
            else:
                if hasattr(img, "size") and hasattr(img, "getdata"):
                    w, h = img.size
                    data = list(img.getdata())
                    frame = [
                        [list(data[y * w + x]) for x in range(w)] for y in range(h)
                    ]
                else:
                    frame = img  # type: ignore
                self._dummy_frames = 0
        log(f"Frame captured: {shape(frame)}", tag="emulator")
        if self._dummy_frames > 3 and self.use_gui:
            log(
                "Restarting emulator due to persistent dummy frames",
                level="WARN",
                tag="emulator",
            )
            self.close()
            self._launch_emulator()
            self._dummy_frames = 0
        if os.getenv("PROFILE") == "dev":
            assert shape(frame) == (144, 160, 3), f"Bad frame shape: {shape(frame)}"
        return frame

    def send_input(self, button: str) -> None:
        """Inject a keypress into the emulator using xdotool."""
        now = time.monotonic()
        if now - self._last_input_time < self.debounce_interval_ms / 1000.0:
            log(f"Input debounced: {button}", level="WARN", tag="emulator")
            return

        if not self.use_gui or not os.getenv("DISPLAY"):
            log(
                "[input] Skipping xdo input: no display available",
                level="WARN",
                tag="emulator",
            )
            return

        try:
            subprocess.run(["xdotool", "key", button], check=False)
        except Exception as e:  # pragma: no cover - runtime safeguard
            log(f"[input] Failed to send {button}: {e}", level="WARN", tag="emulator")
            return

        self._last_input_time = now
        log(f"Input sent: {button}", tag="emulator")

    def close(self) -> None:
        if self.process:
            self.process.terminate()
            self.process.wait()
        log("Emulator closed", tag="emulator")
