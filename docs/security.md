# Security and caveats

- Container runs as a nonroot UID; Kubernetes Pod sets `runAsNonRoot`.
- No service-account automount, privilege escalation, or Linux capabilities.
- Read-only root filesystem; seccomp RuntimeDefault.
- Internal ClusterIP Service; external Ingress disabled by default.
- GitHub Actions has read-only repository access for tests and package write only for image publishing.
- Use immutable SHA tags for reproducible deployments.
- **Not yet implemented:** vulnerability scans, SBOM, admission policies, network policies, TLS and automatic GitOps promotion.
- Pin action commits and base-image digests before using this as a production baseline.
- Do not publish cluster credentials, kubeconfigs, tokens, internal addresses or client data.

The reference service is intended for training and should not be described as production hardened.
