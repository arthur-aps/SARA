#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -d "/usr/local/lib/ollama/cuda_v12" ]; then
    export SARA_USE_GPU=1
    export LD_LIBRARY_PATH="/usr/local/lib/ollama/cuda_v12:$LD_LIBRARY_PATH"
fi

exec "$PROJECT_DIR/venv/bin/python" "$PROJECT_DIR/src/main.py"