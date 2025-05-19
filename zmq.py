import queue
import time

PUB = 1
SUB = 2
SUBSCRIBE = b""
POLLIN = 1

_buses = {}
_next_port = 5500

class Context:
    def socket(self, sock_type):
        return Socket(sock_type)
    def term(self):
        pass

class Socket:
    def __init__(self, sock_type):
        self.type = sock_type
        self.port = None
        self.queue = queue.Queue()

    def bind(self, addr: str):
        port = int(addr.split(':')[-1])
        self.port = port
        _buses.setdefault(port, [])

    def bind_to_random_port(self, addr: str) -> int:
        global _next_port
        port = _next_port
        _next_port += 1
        self.bind(f"tcp://*:{port}")
        return port

    def connect(self, addr: str):
        port = int(addr.split(':')[-1])
        self.port = port
        self.queue = queue.Queue()
        _buses.setdefault(port, []).append(self.queue)

    def setsockopt(self, *args, **kwargs):
        pass

    def send_pyobj(self, obj):
        if self.port is None:
            raise RuntimeError("Socket not bound")
        for q in _buses.get(self.port, []):
            q.put(obj)

    def recv_pyobj(self):
        return self.queue.get()

    def close(self):
        pass

class Poller:
    def __init__(self):
        self.sockets = []
    def register(self, socket, flag):
        self.sockets.append(socket)
    def poll(self, timeout):
        end = time.time() + timeout/1000
        while time.time() < end:
            for s in self.sockets:
                if not s.queue.empty():
                    return [(s, POLLIN)]
            time.sleep(0.01)
        return []
