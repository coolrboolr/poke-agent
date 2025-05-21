from datetime import datetime
import inspect
from pathlib import Path
from typing import Optional


LEVEL_COLORS = {
    "INFO": "\033[94m",  # blue
    "WARN": "\033[93m",  # yellow
    "ERROR": "\033[91m",  # red
}
RESET = "\033[0m"


def log(
    message: str, level: str = "INFO", tag: Optional[str] = None, *, color: bool = True
) -> None:
    """Structured logger with optional color coding."""
    caller = inspect.stack()[1]
    module = tag or caller.frame.f_globals.get("__name__", "__main__").split(".")[-1]
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    prefix = f"[{level.upper()}][{module}][{timestamp}]"
    if color and level.upper() in LEVEL_COLORS:
        prefix = f"{LEVEL_COLORS[level.upper()]}{prefix}{RESET}"
    print(f"{prefix} {message}")


def log_action(action: str, frame_id: int, log_dir: Path = Path("logs")) -> None:
    """Append selected action to actions.log."""
    log_dir.mkdir(exist_ok=True)
    path = log_dir / "actions.log"
    with open(path, "a") as f:
        f.write(f"{frame_id},{action}\n")


def log_latency(
    frame_id: int,
    read_ms: float,
    bus_ms: float,
    decision_ms: float,
    log_dir: Path = Path("logs"),
) -> None:
    """Record latency metrics to latency.csv."""
    log_dir.mkdir(exist_ok=True)
    path = log_dir / "latency.csv"
    exists = path.exists()
    with open(path, "a") as f:
        if not exists:
            f.write("frame,read_ms,bus_ms,decision_ms\n")
        f.write(
            f"{frame_id},{read_ms:.3f},{bus_ms:.3f},{decision_ms:.3f}\n"
        )


