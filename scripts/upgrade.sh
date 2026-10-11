#!/usr/bin/env bash
# Synapse-AG Upgrade Script for macOS and Linux
# Preserves 100% of user data and personal notes; updates only core system files.
set -euo pipefail

REPO_URL="https://github.com/MertAlii/Synapse-AG"
RAW_BASE="https://raw.githubusercontent.com/MertAlii/Synapse-AG/main"

DRY_RUN=false
FORCE=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --force) FORCE=true ;;
        -h|--help)
            echo "Kullanım: ./scripts/upgrade.sh [--dry-run] [--force]"
            exit 0
            ;;
    esac
done

# Sistem dosyaları listesi (GEMINI.md ve kullanıcı notları ASLA EZİLMEZ)
SYSTEM_FILES=(
    ".agents/scripts/_resolve_root.py"
    ".agents/scripts/flush_daily.py"
    ".agents/scripts/inject_context.py"
    ".agents/scripts/compile_knowledge.py"
    ".agents/scripts/companion_compact.py"
    ".agents/scripts/doctor.py"
    ".agents/scripts/yakala.py"
    ".agents/scripts/search_bm25.py"
    ".agents/skills/yakala/SKILL.md"
    ".agents/skills/beyin-doktor/SKILL.md"
    ".agents/hooks.json"
    ".agents/rules/memory-protocol.md"
    ".obsidian/app.json"
    ".obsidian/core-plugins.json"
    ".obsidian/graph.json"
    ".obsidian/daily-notes.json"
    ".obsidian/templates.json"
    ".obsidian/appearance.json"
    "beyin-antigravity.md"
    ".beyin-version"
    "requirements.txt"
    "docs/YAKALA.md"
    "scripts/kur_yakala_windows.ps1"
    "scripts/kur_yakala_macos.sh"
    "scripts/kur_yakala_linux.sh"
    "scripts/upgrade.ps1"
    "scripts/upgrade.sh"
)

# Kök dizini bul
find_root() {
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    if [ -f "$dir/.beyin-version" ]; then
        echo "$dir"
        return
    fi
    local cur="$PWD"
    while [ "$cur" != "/" ]; do
        if [ -f "$cur/.beyin-version" ]; then
            echo "$cur"
            return
        fi
        cur="$(dirname "$cur")"
    done
    echo "$HOME/.gemini/antigravity/scratch/synapse-ag"
}

ROOT="$(find_root)"
if [ ! -f "$ROOT/.beyin-version" ]; then
    echo "[X] Synapse-AG kök dizini bulunamadı (.beyin-version aranıyor)." >&2
    exit 1
fi

CURRENT_VER="$(cat "$ROOT/.beyin-version" | tr -d '[:space:]')"

echo "=========================================================="
echo "          SYNAPSE-AG SİSTEM GÜNCELLEYİCİ (v3)"
echo "=========================================================="
echo "Kök Dizin     : $ROOT"
echo "Mevcut Sürüm  : $CURRENT_VER"

# Uzak sürümü kontrol et
REMOTE_VER=""
if command -v curl >/dev/null 2>&1; then
    REMOTE_VER="$(curl -fsSL "$RAW_BASE/.beyin-version" 2>/dev/null | tr -d '[:space:]' || true)"
elif command -v wget >/dev/null 2>&1; then
    REMOTE_VER="$(wget -qO- "$RAW_BASE/.beyin-version" 2>/dev/null | tr -d '[:space:]' || true)"
fi

if [ -n "$REMOTE_VER" ]; then
    echo "En Son Sürüm  : $REMOTE_VER"
    if [ "$CURRENT_VER" = "$REMOTE_VER" ] && [ "$FORCE" = false ]; then
        echo "[OK] Zaten en güncel sürümü ($CURRENT_VER) kullanıyorsunuz."
        echo "     Zorla yeniden yüklemek için: ./scripts/upgrade.sh --force"
        exit 0
    fi
else
    echo "[!] Uzak sürüm kontrol edilemedi (çevrimdışı veya GitHub erişimi yok)."
fi

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Güncellenecek sistem dosyaları:"
    for f in "${SYSTEM_FILES[@]}"; do
        echo "  - $f"
    done
    echo "[DRY-RUN] Kullanıcı notları, projeler ve hafıza korunacaktır."
    exit 0
fi

# Yedek al
TIMESTAMP="$(date +%Y-%m-%d_%H%M%S)"
BACKUP_DIR="$ROOT/.bak-$TIMESTAMP"
echo "[*] Güvenlik yedeği oluşturuluyor: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

for f in "${SYSTEM_FILES[@]}"; do
    if [ -f "$ROOT/$f" ]; then
        mkdir -p "$BACKUP_DIR/$(dirname "$f")"
        cp "$ROOT/$f" "$BACKUP_DIR/$f"
    fi
done

# Güncellemeleri indir
echo "[*] Sistem dosyaları güncelleniyor..."
FAIL_COUNT=0

for f in "${SYSTEM_FILES[@]}"; do
    TARGET="$ROOT/$f"
    URL="$RAW_BASE/$f"
    mkdir -p "$(dirname "$TARGET")"
    
    if command -v curl >/dev/null 2>&1; then
        if curl -fsSL "$URL" -o "$TARGET.tmp" 2>/dev/null; then
            mv "$TARGET.tmp" "$TARGET"
            echo "  [OK] $f"
        else
            rm -f "$TARGET.tmp"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        fi
    fi
done

# İzinleri ayarla
chmod +x "$ROOT/scripts/"*.sh 2>/dev/null || true

echo "=========================================================="
if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "[BAŞARILI] Synapse-AG başarıyla güncellendi!"
else
    echo "[UYARI] Bazı dosyalar indirilemedi ($FAIL_COUNT adet)."
fi
echo "Yedek Konumu : $BACKUP_DIR"
echo "Kişisel Notlar ve Veriler: %100 KORUNDU"
echo "=========================================================="
