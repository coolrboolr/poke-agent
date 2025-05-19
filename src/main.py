import os
from dotenv import load_dotenv

from src.utils.logger import log
from src.emulator.adapter import EmulatorAdapter


def main() -> None:
    """Entry point for poke-streamer."""
    load_dotenv()
    _ = os.getenv("TWITCH_STREAM_KEY")

    try:
        adapter = EmulatorAdapter()
    except FileNotFoundError as exc:
        log(str(exc), level="ERROR")
        return

    log("Emulator ready")
    frame = adapter.read_frame()
    log(f"Frame received: {frame.shape}")


if __name__ == "__main__":
    main()
