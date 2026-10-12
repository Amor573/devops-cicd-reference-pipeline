# Operational runbook

Review the target context before changing anything: `kubectl config current-context` or `oc whoami`.

1. Confirm image in GHCR and registry visibility or imagePullSecret.
2. Run `helm lint charts/platform-demo` and `helm template platform-demo charts/platform-demo`.
3. Install with `helm upgrade --install platform-demo charts/platform-demo -n platform-demo --create-namespace`.
4. Verify with `kubectl rollout status deployment/platform-demo-platform-demo -n platform-demo`.
5. Inspect pods and events with `kubectl get pods,events -n platform-demo`.
6. `ImagePullBackOff`: review tag, registry permissions and pull secrets.
7. `CrashLoopBackOff`: inspect exit code, `kubectl logs --previous` and security context.
8. `Pending`: inspect scheduler events and CPU/memory constraints.
9. Roll back safely: `helm history platform-demo -n platform-demo`, then `helm rollback platform-demo <REVISION> -n platform-demo`.

For a smoke test: port-forward the service to localhost:8080 and run `bash scripts/smoke-test.sh`.

**No live cluster run has been verified for this repository yet.**
