#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
    echo "Criando .env..."
    cp .env.example .env
fi

if [ ! -f sara-esp-server/src/secrets.h ]; then
    echo "Criando secrets.h..."
    cp secrets.h.example sara-esp-server/src/secrets.h
fi