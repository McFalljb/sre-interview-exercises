"""Hit counter service backed by Redis."""
import hmac
import json
import logging
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import settings
from redis_client import Redis

log = logging.getLogger("app")
redis = Redis(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_TIMEOUT)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            try:
                redis.ping()
            except Exception as exc:
                self.reply(503, {"status": "unavailable", "redis": str(exc)})
                return
            self.reply(200, {"status": "ok", "redis": "ok"})
        elif self.path == "/":
            self.reply(200, {"hits": redis.command("INCR", "hits")})
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/reset":
            self.reply(404, {"error": "not found"})
            return
        expected = f"Bearer {settings.API_TOKEN}"
        given = self.headers.get("Authorization", "")
        if not settings.API_TOKEN or not hmac.compare_digest(given, expected):
            self.reply(403, {"error": "forbidden"})
            return
        redis.command("SET", "hits", 0)
        self.reply(200, {"hits": 0})

    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        log.info("%s %s", self.address_string(), fmt % args)


def main():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    try:
        redis.ping()
    except Exception as exc:
        log.error("cannot reach redis at %s:%s: %s", settings.REDIS_HOST, settings.REDIS_PORT, exc)
        sys.exit(1)
    log.info("connected to redis at %s:%s", settings.REDIS_HOST, settings.REDIS_PORT)

    server = ThreadingHTTPServer((settings.HOST, settings.PORT), Handler)
    log.info("listening on %s:%s", settings.HOST, settings.PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        log.info("stopped")


if __name__ == "__main__":
    main()
