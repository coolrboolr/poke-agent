import json
import os
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv

from src.arbiter import select_action
from src.utils.actions import Action
from src.memory.core import ContextMemory

from src.emulator.adapter import EmulatorAdapter
from src.emulator.frame_bus import FrameBus
from src.utils.logger import log
from src.rl import RLCritic
from src.game_profiles.registry import load_profile


def run_loop(duration_s: int = 30) -> None:
    adapter = EmulatorAdapter()
    bus = FrameBus()
    context = ContextMemory()
    critic = RLCritic()
    profile = load_profile()

    frames = 0
    read_lat = []
    bus_lat = []
    decision_lat = []
    start = time.time()

    first_shape = None
    prev_state = {}
    last_action: Action | None = None
    while time.time() - start < duration_s:
        t0 = time.time()
        frame = adapter.read_frame()
        t1 = time.time()
        game_state = profile.parse_game_state(frame)
        context.update(game_state)
        a_start = time.time()
        action = select_action(game_state, context)
        a_end = time.time()
        if action:
            adapter.send_input(action.value)
            log(f"Selected action {action}", tag="main")
        if first_shape is None:
            from src.array_utils import shape

            first_shape = shape(frame)
            if first_shape != (160, 144, 3):
                log(f"Unexpected frame shape {first_shape}", level="WARN", tag="main")
        bus.publish(frame)

        reward = profile.get_reward(prev_state, game_state)
        critic.observe(prev_state, last_action, reward)
        critic.estimate_value(game_state)
        prev_state = game_state
        last_action = action

        overlay = {
            "mode": game_state.get("mode", "idle"),
            "action": action.value if action else None,
        }
        try:
            Path("overlay.json").write_text(json.dumps(overlay))
        except Exception:
            pass
        t2 = time.time()
        frames += 1
        read_lat.append((t1 - t0) * 1000)
        decision_lat.append((a_end - a_start) * 1000)
        bus_lat.append((t2 - t1) * 1000)

    bus.close()
    adapter.close()

    avg_fps = frames / duration_s
    avg_read = sum(read_lat) / len(read_lat)
    avg_bus = sum(bus_lat) / len(bus_lat)
    avg_decision = sum(decision_lat) / len(decision_lat) if decision_lat else 0.0

    metrics = {
        "average_fps": avg_fps,
        "avg_frame_read_ms": avg_read,
        "avg_bus_publish_ms": avg_bus,
        "avg_decision_ms": avg_decision,
    }
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    with open(logs_dir / "loop_metrics.json", "w") as f:
        json.dump(metrics, f)

    log(
        f"Loop complete FPS={avg_fps:.2f} read={avg_read:.1f}ms bus={avg_bus:.1f}ms decision={avg_decision:.1f}ms",
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
        subprocess.Popen(
            ["python", "tools/frame_diagnose.py"], stdout=subprocess.DEVNULL
        )
        log("Dev profile enabled", tag="main")

    try:
        run_loop(duration_s=duration)
    except FileNotFoundError as exc:
        log(str(exc), level="ERROR", tag="main")
        return


if __name__ == "__main__":
    main()
