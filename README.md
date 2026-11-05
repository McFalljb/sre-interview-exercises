# SRE Interview Exercises

The interview has two parts:

1. **Discussion:** five open-ended questions, listed in [`QUESTIONS.md`](QUESTIONS.md).
2. **Hands-on:** one of the three problems below.

## Hands-on problems

Pick **one** of the three problems below and solve it in about 30 minutes. You'll work on your own laptop and talk through what you're doing as you go.

| Problem | Folder | You'll need |
| --- | --- | --- |
| Terraform | [`terraform/`](terraform/) | Terraform 1.5+ |
| Kubernetes | [`kubernetes/`](kubernetes/) | Docker, kind, kubectl |
| Docker | [`docker/`](docker/) | Docker with Compose v2 or later, curl |

Each folder has its own README with the problem, the goal and the commands you'll need. There's no automated test: you decide when you think you're done, then walk us through it.

## Before the interview

1. Clone this repo.
2. Install the tools for the problem(s) you might pick. Give Docker at least 4 GB of memory.
3. **Kubernetes:** create the local cluster beforehand with the setup commands in [`kubernetes/README.md`](kubernetes/README.md#before-the-interview). It takes a few minutes, and you don't want to spend interview time on it.
4. **Docker:** pull the base images: `docker pull python:3.12-slim` and `docker pull redis:7.4.1-alpine`.
5. **Terraform:** run `terraform init` in `terraform/` (it downloads one small provider).

You don't need a cloud account or credentials for any of these.

## During the interview

- Use whatever tools you normally would, including AI assistants. If you use AI, tell us what you're asking it and why.
- Explain your reasoning as you go. We care more about how you work through the problem than about finishing.
- If you finish early, each README lists an extra thing or two to try.
