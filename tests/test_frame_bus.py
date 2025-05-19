from src.array_utils import zeros, array_equal
import zmq

from src.emulator.frame_bus import FrameBus


def test_pub_sub_frame():
    bus = FrameBus(port=0)
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://127.0.0.1:{bus.port}")
    sub.setsockopt(zmq.SUBSCRIBE, b"")

    frame = zeros((2, 2, 3))
    bus.publish(frame)

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    socks = dict(poller.poll(1000))
    assert sub in socks
    received = sub.recv_pyobj()
    assert array_equal(received, frame)

    sub.close()
    bus.close()
    ctx.term()

