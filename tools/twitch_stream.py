import os
import subprocess
import zmq
import numpy as np

from src.utils.logger import log


def main() -> None:
    key = os.getenv("TWITCH_STREAM_KEY")
    if not key:
        raise RuntimeError("TWITCH_STREAM_KEY not set")

    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    port = int(os.getenv("FRAMEBUS_PORT", "5555"))
    sub.connect(f"tcp://127.0.0.1:{port}")
    sub.setsockopt(zmq.SUBSCRIBE, b"")

    ffmpeg_cmd = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "160x144",
        "-r",
        "60",
        "-i",
        "-",
        "-vf",
        "scale=1280:720",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-tune",
        "zerolatency",
        "-pix_fmt",
        "yuv420p",
        "-f",
        "flv",
        f"rtmp://live.twitch.tv/app/{key}",
    ]

    log("Starting Twitch stream", tag="stream")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    try:
        while True:
            frame = sub.recv_pyobj()
            arr = np.array(frame, dtype=np.uint8)
            proc.stdin.write(arr.tobytes())
    except KeyboardInterrupt:
        log("Stream interrupted", tag="stream")
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.wait()
        sub.close()
        ctx.term()
        log("Streamer shut down", tag="stream")


if __name__ == "__main__":
    main()
