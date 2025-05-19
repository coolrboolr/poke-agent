import os
from dotenv import load_dotenv

from src.utils.logger import log


def main() -> None:
    """Entry point for poke-streamer."""
    load_dotenv()
    # Access environment variables if needed
    _ = os.getenv("ROM_PATH")
    _ = os.getenv("TWITCH_STREAM_KEY")
    log("Agent initialized. Ready for M1.")


if __name__ == "__main__":
    main()
