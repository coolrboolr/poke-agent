import json
import os
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv

from src.emulator.adapter import EmulatorAdapter
from src.emulator.frame_bus import FrameBus
from src.utils.logger import log


def run_loop(duration_s: int = 30) -> None:
    adapter = EmulatorAdapter()
    bus = FrameBus()

    frames = 0
    read_lat = []
    bus_lat = []
    start = time.time()

    first_shape = None
    while time.time() - start < duration_s:
        t0 = time.time()
        frame = adapter.read_frame()
        t1 = time.time()
        if first_shape is None:
            first_shape = frame.shape
            if first_shape != (160, 144, 3):
                log(f"Unexpected frame shape {first_shape}", level="WARN", tag="main")
        bus.publish(frame)
        t2 = time.time()
        frames += 1
        read_lat.append((t1 - t0) * 1000)
        bus_lat.append((t2 - t1) * 1000)

    bus.close()
    adapter.close()

    avg_fps = frames / duration_s
    avg_read = sum(read_lat) / len(read_lat)
    avg_bus = sum(bus_lat) / len(bus_lat)

    metrics = {
        "average_fps": avg_fps,
        "avg_frame_read_ms": avg_read,
        "avg_bus_publish_ms": avg_bus,
    }
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    with open(logs_dir / "loop_metrics.json", "w") as f:
        json.dump(metrics, f)

    log(
        f"Loop complete FPS={avg_fps:.2f} read={avg_read:.1f}ms bus={avg_bus:.1f}ms",
        tag="main",
    )
    if avg_fps < 5.0 or avg_read > 100 or avg_bus > 100:
        log("Performance warning: low FPS or high latency", level="WARN", tag="main")


def main() -> None:
    """Entry point for poke-streamer."""
    load_dotenv()
    profile = os.getenv("PROFILE", "release")
    duration = int(os.getenv("LOOP_DURATION", "30"))

    if profile == "dev":
        subprocess.Popen(["python", "tools/frame_diagnose.py"], stdout=subprocess.DEVNULL)
        log("Dev profile enabled", tag="main")

    try:
        run_loop(duration_s=duration)
    except FileNotFoundError as exc:
        log(str(exc), level="ERROR", tag="main")
        return


if __name__ == "__main__":
    main()
