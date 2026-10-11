#!/usr/bin/env bash
# Synapse-AG Master CLI Runner for macOS & Linux
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TUI_SCRIPT="$VAULT_DIR/.agents/scripts/tui.py"
YAKALA_SCRIPT="$VAULT_DIR/.agents/scripts/yakala.py"
DOCTOR_SCRIPT="$VAULT_DIR/.agents/scripts/doctor.py"

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[X] python3 bulunamadı." >&2
    exit 1
fi

CMD="${1:-tui}"

case "$CMD" in
    tui)
        "$PYTHON_BIN" "$TUI_SCRIPT"
        ;;
    doctor|doktor)
        "$PYTHON_BIN" "$DOCTOR_SCRIPT"
        ;;
    yakala)
        shift || true
        "$PYTHON_BIN" "$YAKALA_SCRIPT" "$@"
        ;;
    search)
        shift || true
        "$PYTHON_BIN" "$TUI_SCRIPT" --search "$*"
        ;;
    devil)
        shift || true
        "$PYTHON_BIN" "$TUI_SCRIPT" --devil "$*"
        ;;
    *)
        "$PYTHON_BIN" "$TUI_SCRIPT" "$@"
        ;;
esac
