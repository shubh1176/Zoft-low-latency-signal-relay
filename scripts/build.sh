#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
BUILD_DIR="$ROOT_DIR/build/cpp"

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake "$ROOT_DIR/cpp" -DCMAKE_BUILD_TYPE=Release "$@"
cmake --build . --target parity_daemon
