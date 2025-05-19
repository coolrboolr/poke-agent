from datetime import datetime
import inspect


def log(message: str, level: str = "INFO") -> None:
    """Basic logger printing timestamp, level and module name."""
    caller = inspect.stack()[1]
    module = caller.frame.f_globals.get("__name__", "__main__")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} [{level}] {module}: {message}")
