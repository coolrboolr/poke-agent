import argparse
import time
from pathlib import Path

import numpy as np
from PIL import Image
import zmq

from src.utils.logger import log


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5555)
    parser.add_argument("--save-frame", action="store_true")
    args = parser.parse_args()

    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://127.0.0.1:{args.port}")
    sub.setsockopt(zmq.SUBSCRIBE, b"")

    log("Diagnostic tool connected", tag="diagnose")
    try:
        while True:
            frame = sub.recv_pyobj()
            ts = time.time()
            if isinstance(frame, np.ndarray):
                log(f"Frame {frame.shape} at {ts}", tag="diagnose")
                if args.save_frame:
                    img = Image.fromarray(frame)
                    Path("logs").mkdir(exist_ok=True)
                    img.save(Path("logs") / f"diag_{int(ts)}.png")
            else:
                log("Received invalid frame", level="WARN", tag="diagnose")
    except KeyboardInterrupt:
        pass
    finally:
        sub.close()
        ctx.term()


if __name__ == "__main__":
    main()
