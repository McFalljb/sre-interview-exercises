"""Just enough of the Redis protocol (RESP) for this service."""
import socket


class RedisError(Exception):
    pass


class Redis:
    def __init__(self, host, port, timeout=1.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def command(self, *args):
        payload = f"*{len(args)}\r\n".encode()
        for arg in args:
            data = str(arg).encode()
            payload += b"$%d\r\n%s\r\n" % (len(data), data)
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as sock:
            sock.sendall(payload)
            reply = sock.makefile("rb").readline().rstrip(b"\r\n").decode()
        kind, value = reply[:1], reply[1:]
        if kind == "-":
            raise RedisError(value)
        if kind == ":":
            return int(value)
        if kind == "+":
            return value
        raise RedisError(f"unexpected reply: {reply!r}")

    def ping(self):
        return self.command("PING") == "PONG"
