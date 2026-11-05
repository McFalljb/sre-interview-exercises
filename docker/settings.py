import os

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8080"))

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_TIMEOUT = float(os.environ.get("REDIS_TIMEOUT", "1.0"))

API_TOKEN = os.environ.get("API_TOKEN", "")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
