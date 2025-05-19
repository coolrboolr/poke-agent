import zmq
import numpy as np
from src.utils.logger import log


class FrameBus:
    """ZeroMQ PUB socket broadcasting frames."""

    def __init__(self, port: int = 5555) -> None:
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        if port == 0:
            self.port = self.socket.bind_to_random_port("tcp://*")
        else:
            self.port = port
            self.socket.bind(f"tcp://*:{port}")
        log(f"FrameBus bound to port {self.port}", tag="bus")

    def publish(self, frame: np.ndarray) -> None:
        self.socket.send_pyobj(frame)
        log(f"Published frame {frame.shape}", tag="bus")

    def close(self) -> None:
        self.socket.close()
        self.context.term()
        log("FrameBus closed", tag="bus")
