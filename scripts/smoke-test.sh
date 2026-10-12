#!/usr/bin/env bash
set -euo pipefail
base="${1:-http://localhost:8080}"
echo "Checking $base ..."
curl --fail --silent --show-error "${base%/}/healthz"
curl --fail --silent --show-error "${base%/}/readyz"
curl --fail --silent --show-error "${base%/}/"
echo "Smoke checks passed"
