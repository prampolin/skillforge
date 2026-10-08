#!/usr/bin/env bash
# No model invocation occurs without an explicit --run argument.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/run-eval-001.py" "$@"
