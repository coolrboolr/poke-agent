from datetime import datetime
import inspect
from typing import Optional


LEVEL_COLORS = {
    "INFO": "\033[94m",  # blue
    "WARN": "\033[93m",  # yellow
    "ERROR": "\033[91m",  # red
}
RESET = "\033[0m"


def log(message: str, level: str = "INFO", tag: Optional[str] = None, *, color: bool = True) -> None:
    """Structured logger with optional color coding."""
    caller = inspect.stack()[1]
    module = tag or caller.frame.f_globals.get("__name__", "__main__").split(".")[-1]
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    prefix = f"[{level.upper()}][{module}][{timestamp}]"
    if color and level.upper() in LEVEL_COLORS:
        prefix = f"{LEVEL_COLORS[level.upper()]}{prefix}{RESET}"
    print(f"{prefix} {message}")
