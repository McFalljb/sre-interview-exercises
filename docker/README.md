# Docker: containerize a small service

`app.py` is a small hit-counter web service that stores its data in Redis.
It's written in plain Python (standard library only) and is configured with
environment variables (see `settings.py`).

| Endpoint | What it does |
| --- | --- |
| `GET /health` | `200 {"status": "ok", "redis": "ok"}` when the service can reach Redis, `503` otherwise |
| `GET /` | Increments and returns the hit counter |
| `POST /reset` | Resets the counter (needs `Authorization: Bearer <API_TOKEN>`) |

The `Dockerfile` was started but never finished, and there is no Compose file yet.

## Requirements

- Docker with Compose v2 or later (`docker compose version`)
- `curl`
- Port 8080 free on your machine

Before the interview, pull the base images:
`docker pull python:3.12-slim` and `docker pull redis:7.4.1-alpine`.

## Task

1. Finish the `Dockerfile` so the image runs the service.
2. Write `compose.yaml` in this folder that runs the stack:
   - a service named `app`, built from this folder's `Dockerfile`
   - a service named `redis`, using the official `redis` image (pin a version)
   - the app published on host port **8080**

You can edit any file in this folder except `ci/`.

## Goal

When the stack is run with the commands below:

- `curl http://localhost:8080/health` returns `200` with `"redis": "ok"`;
- the built image contains nothing from `.env` (keep the file: it holds local
  settings);
- stopping the stack (the `stop -t 10` command below) takes under 5 seconds,
  and the app exits on its own rather than being killed (check the exit code
  in `ps -a`: 137 means it was killed).

Tell us when you think you're done, and be ready to explain what you changed
and why.

## Commands

CI runs the stack with an overlay that simulates Redis loading a real dataset
at startup, and stops it with a 10-second timeout. Run it the same way:

```sh
docker compose -f compose.yaml -f ci/slow-redis.yaml up --build -d
curl -i http://localhost:8080/health     # give the app a second to start first
docker compose -f compose.yaml -f ci/slow-redis.yaml ps -a
docker compose -f compose.yaml -f ci/slow-redis.yaml logs app
time docker compose -f compose.yaml -f ci/slow-redis.yaml stop -t 10
docker compose -f compose.yaml -f ci/slow-redis.yaml down --rmi local    # clean up
```

## If you finish early

Pick one and talk through the trade-offs:

- Run the app as a non-root user.
- Make the image smaller, and make rebuilds after a code change faster.
- Keep the Redis data across `docker compose down` and `up`.
