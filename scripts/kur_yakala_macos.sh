#!/usr/bin/env bash
# Synapse-AG macOS 'Beyne At' Entegrasyon Kurucusu
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
YAKALA_SCRIPT="$VAULT_DIR/.agents/scripts/yakala.py"

echo "=========================================================="
echo "    SYNAPSE-AG macOS 'BEYNE AT' ENTEGRASYONU"
echo "=========================================================="
echo "Kasa Dizini   : $VAULT_DIR"
echo "Yakala Betiği : $YAKALA_SCRIPT"

# 1. Python yorumlayıcısını bul
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[X] python3 bulunamadı. Lütfen Python yükleyin." >&2
    exit 1
fi

# 2. Web Clipper şablonunu oluştur
echo "[*] Obsidian Web Clipper şablonu oluşturuluyor..."
"$PYTHON_BIN" "$YAKALA_SCRIPT" sablon

# 3. macOS Automator / Quick Action & LaunchAgent veya CLI wrapper oluştur
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
WRAPPER="$BIN_DIR/beyne-at"

cat <<EOF > "$WRAPPER"
#!/usr/bin/env bash
# Synapse-AG macOS Yakalama Wrapper
if [ \$# -gt 0 ]; then
    "$PYTHON_BIN" "$YAKALA_SCRIPT" "\$@"
else
    "$PYTHON_BIN" "$YAKALA_SCRIPT" --clipboard
fi
EOF

chmod +x "$WRAPPER"

echo "[OK] macOS CLI aracı kuruldu: $WRAPPER"
echo ""
echo "Kullanım ve İpuçları:"
echo "  1. CLI ile panoyu yakala:"
echo "     beyne-at"
echo "  2. Finder'dan dosya veya link yakala:"
echo "     beyne-at /yol/dosya.pdf --note 'Önemli döküman'"
echo "  3. macOS Kısayollar (Shortcuts.app):"
echo "     - Kısayollar uygulamasını açın -> Yeni Kısayol ('Beyne At')."
echo "     - 'Kabuk Betiği Çalıştır' (Run Shell Script) eylemi ekleyin."
echo "     - Komut: $WRAPPER"
echo "     - Kısayol Tuşu ata: Control+Option+B"
echo "  4. Obsidian Web Clipper:"
echo "     - Tarayıcıda eklentiyi kurun (https://obsidian.md/clipper)."
echo "     - 000-Inbox/Yakala/beyne-at-web-clipper.json dosyasını içe aktarın."
echo "=========================================================="
