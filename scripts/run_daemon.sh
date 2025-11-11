#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

"$ROOT_DIR/scripts/build.sh"

cd "$ROOT_DIR/python"
python3 daemon.py
