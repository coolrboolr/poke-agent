import time
import tracemalloc

from src.main import run_loop
from src.utils.logger import log


def main() -> None:
    """Run the agent for an extended soak test."""
    duration = 30 * 60
    tracemalloc.start()
    start = time.time()
    while time.time() - start < duration:
        loop_end = min(duration - (time.time() - start), 60)
        run_loop(duration_s=int(loop_end))
        current, peak = tracemalloc.get_traced_memory()
        log(
            f"Memory usage: {current / 1_048_576:.2f}MB peak={peak / 1_048_576:.2f}MB",
            tag="stress",
        )
    tracemalloc.stop()


if __name__ == "__main__":
    main()
