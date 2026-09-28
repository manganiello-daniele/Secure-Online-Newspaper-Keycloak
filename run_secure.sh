#!/usr/bin/env bash
set -euo pipefail

export VAULT_ADDR="${VAULT_ADDR:-http://127.0.0.1:8200}"

: "${VAULT_TOKEN:?Set VAULT_TOKEN before running this script}"

export FLASK_SECRET_KEY="$(vault kv get -field=SECRET_KEY project/flask)"
export SQLALCHEMY_DATABASE_URI="$(vault kv get -field=URI project/postgres)"

if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
fi

python app.py
