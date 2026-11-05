"""orders-api: a tiny HTTP service used for the Kubernetes exercise.

Endpoints:
  GET /           service info (which pod answered)
  GET /orders     a few fake orders
  GET /healthz    200 once the service has finished warming up, 503 before
"""

import json
import os
import signal
import socket
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8080"))
CACHE_MB = int(os.environ.get("CACHE_MB", "96"))
HOSTNAME = socket.gethostname()

state = {"ready": False, "cache": None}


def log(msg):
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {HOSTNAME} {msg}", flush=True)


def warm_cache():
    log(f"loading product catalog into memory ({CACHE_MB} MiB)")
    state["cache"] = b"\x01" * (CACHE_MB * 1024 * 1024)
    time.sleep(2)
    state["ready"] = True
    log("catalog loaded, ready to serve")


class Handler(BaseHTTPRequestHandler):
    server_version = "orders-api/1.0"

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/healthz":
            if state["ready"]:
                self._send(200, {"status": "ok"})
            else:
                self._send(503, {"status": "warming up"})
        elif self.path == "/":
            self._send(200, {"service": "orders-api", "pod": HOSTNAME})
        elif self.path == "/orders":
            self._send(200, {"pod": HOSTNAME, "orders": [
                {"id": 1001, "sku": "WIDGET-1", "qty": 2},
                {"id": 1002, "sku": "GADGET-7", "qty": 1},
            ]})
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        pass


def handle_sigterm(signum, frame):
    log("received SIGTERM, shutting down")
    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, handle_sigterm)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    threading.Thread(target=warm_cache, daemon=True).start()
    log(f"listening on :{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
