import time

from src.emulator.adapter import EmulatorAdapter
from src.emulator.frame_bus import FrameBus
from src.utils.logger import log


def main() -> None:
    adapter = EmulatorAdapter()
    bus = FrameBus()
    log("Starting frame stream")
    try:
        while True:
            frame = adapter.read_frame()
            bus.publish(frame)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        bus.close()
        adapter.close()


if __name__ == "__main__":
    main()
