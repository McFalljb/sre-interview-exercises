# Kubernetes: orders-api won't come up

`orders-api` is a small HTTP service. The team moved it onto the shared
Kubernetes platform and it has never served a request there.

A local [kind](https://kind.sigs.k8s.io/) cluster stands in for the real
platform: one control-plane node and three worker nodes. Traffic from your
laptop enters through a NodePort on the control-plane node
(`http://127.0.0.1:30080`) and goes through the Service, the same way a load
balancer would reach it.

## Before the interview

Prerequisites:

- Docker (Docker Desktop, OrbStack, Colima or Docker Engine), running, with at
  least **4 GB of memory and 2 CPUs** available to it
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) v0.32 or newer
- `kubectl` v1.35 or newer
- Free host port `30080`

From this folder, create the cluster, build the app image and load it into the
nodes. The first run takes a few minutes.

```sh
kind create cluster --name sre-k8s-exercise --config kind-config.yaml --wait 3m
docker build -t orders-api:1.0.0 app/
kind load docker-image orders-api:1.0.0 --name sre-k8s-exercise
kubectl --context kind-sre-k8s-exercise wait --for=condition=Ready node --all --timeout=3m
```

`kind create cluster` switches your current kubectl context to
`kind-sre-k8s-exercise`. Every command below passes `--context` explicitly. If
you leave it out, first check that `kubectl config current-context` prints
`kind-sre-k8s-exercise` and not a real cluster.

## Task

Get `orders-api` serving by fixing the manifests in `k8s/`. If you decide to
change `app/` instead, be ready to explain why.

## Goal

```sh
curl -i http://127.0.0.1:30080/
```

returns HTTP 200. Tell us when you think you're done, and explain what you
found, how you found it and why your fix works.

## Commands

```sh
kubectl --context kind-sre-k8s-exercise apply -f k8s/
kubectl --context kind-sre-k8s-exercise -n orders get pods,svc,endpointslices -o wide
kubectl --context kind-sre-k8s-exercise -n orders describe pod -l app.kubernetes.io/name=orders-api
kubectl --context kind-sre-k8s-exercise -n orders logs -l app.kubernetes.io/name=orders-api --prefix
kubectl --context kind-sre-k8s-exercise -n orders rollout status deploy/orders-api --timeout=60s
kubectl --context kind-sre-k8s-exercise -n orders get events --sort-by=.lastTimestamp
```

If you change anything under `app/`, rebuild and reload the image (the
`docker build` and `kind load` commands above), then
`kubectl --context kind-sre-k8s-exercise -n orders rollout restart deploy/orders-api`.

When you're finished: `kind delete cluster --name sre-k8s-exercise`.

## If you finish early

Which probes (startup, readiness, liveness) would you add for an app that
takes a few seconds to warm up, and how would you size its requests and
limits?

## Troubleshooting setup

- Port 30080 already in use: stop whatever is using it, delete the cluster and
  create it again.
- Pods stuck in `ErrImagePull` / `ImagePullBackOff` for `orders-api:1.0.0`: run
  the `kind load` command again.
- On Linux, cluster creation fails with "too many open files": see kind's
  [known issues](https://kind.sigs.k8s.io/docs/user/known-issues/#pod-errors-due-to-too-many-open-files).
