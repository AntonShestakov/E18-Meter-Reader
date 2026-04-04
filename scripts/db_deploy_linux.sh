#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ENV_FILE="$ROOT_DIR/.env.local"
if [[ -f "$ENV_FILE" ]]; then
  echo "Loading environment from $ENV_FILE"
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "ERROR: DATABASE_URL is not set. Please create .env.local with DATABASE_URL."
  exit 1
fi

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  echo "WARNING: TELEGRAM_BOT_TOKEN is not set. Set it in .env.local if you want to run the bot."
fi

if [[ ! -d "venv" ]]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -e .

if [[ -z "${FLYWAY_URL:-}" || -z "${FLYWAY_USER:-}" || -z "${FLYWAY_PASSWORD:-}" ]]; then
  if [[ "$DATABASE_URL" =~ ^postgresql://([^:]+):([^@]+)@([^:/]+)(:([0-9]+))?/([^?]+) ]]; then
    export FLYWAY_URL="jdbc:postgresql://${BASH_REMATCH[3]}:${BASH_REMATCH[5]:-5432}/${BASH_REMATCH[6]}"
    export FLYWAY_USER="${BASH_REMATCH[1]}"
    export FLYWAY_PASSWORD="${BASH_REMATCH[2]}"
    echo "Derived Flyway configuration from DATABASE_URL."
  else
    echo "ERROR: Could not parse DATABASE_URL for Flyway config."
    exit 1
  fi
fi

if ! command -v flyway >/dev/null 2>&1; then
  echo "ERROR: flyway CLI not found on PATH. Install Flyway or use Docker."
  exit 1
fi

flyway -locations=filesystem:migrations migrate

echo "Deployment complete. Bot dependencies installed and Flyway migrations applied."
