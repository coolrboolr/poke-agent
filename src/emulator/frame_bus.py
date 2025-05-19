import zmq
import numpy as np


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

    def publish(self, frame: np.ndarray) -> None:
        self.socket.send_pyobj(frame)

    def close(self) -> None:
        self.socket.close()
        self.context.term()
