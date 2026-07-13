#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "A SARA não vai funcionar se os arquivos .example não estiverem corretos. Verifique-os antes de continuar!"
echo "Deseja continuar? (s/N)"
while true; do
read -rsn1 key

case $key in
s|S)
break
;;

*)
exit 0
;;
esac

done

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

echo
echo "Setup concluído. Deseja executar o programa? (s/N)"
while true; do
read -rsn1 key

case $key in
s|S)
break
;;

*)
exit 0
;;
esac

done

./scripts/run.sh