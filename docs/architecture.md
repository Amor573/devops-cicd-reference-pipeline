# Architecture and delivery stages

The repository provides a single-process, standard-library HTTP server; no external runtime dependencies or data services are required.

1. A pull request or push triggers Python tests and Helm chart lint/render checks.
2. Only a successful push to `main` should publish a container image to GHCR.
3. Operators use Helm to deploy the image into their own Kubernetes or OpenShift environment.
4. Readiness, liveness, logs, HTTP smoke test and simple Prometheus-format counters provide basic validation.

**Trade-offs:** metrics are in-memory per-process counters, readiness only checks process responsiveness, and the workflow has no cluster credentials. A successful CI run does not prove a cluster deployment.
