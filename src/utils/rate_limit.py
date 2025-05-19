from time import monotonic
from typing import Callable


def rate_limit(interval_ms: int) -> Callable[[Callable], Callable]:
    """Decorator to prevent a function from being called more than once every interval."""
    def decorator(func: Callable) -> Callable:
        last_call = 0.0

        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = monotonic()
            if now - last_call >= interval_ms / 1000.0:
                last_call = now
                return func(*args, **kwargs)
        return wrapper

    return decorator
