#!/usr/bin/env bash
# Synapse-AG Linux 'Beyne At' Entegrasyon Kurucusu
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
YAKALA_SCRIPT="$VAULT_DIR/.agents/scripts/yakala.py"

echo "=========================================================="
echo "    SYNAPSE-AG LINUX 'BEYNE AT' ENTEGRASYONU"
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

# 3. CLI wrapper oluştur (~/.local/bin/beyne-at)
BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
mkdir -p "$BIN_DIR"
WRAPPER="$BIN_DIR/beyne-at"

cat <<EOF > "$WRAPPER"
#!/usr/bin/env bash
# Synapse-AG Linux Yakalama Wrapper
if [ \$# -gt 0 ]; then
    "$PYTHON_BIN" "$YAKALA_SCRIPT" "\$@"
else
    "$PYTHON_BIN" "$YAKALA_SCRIPT" --clipboard
fi
EOF

chmod +x "$WRAPPER"

# 4. .desktop girişi oluştur
APPS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
mkdir -p "$APPS_DIR"
DESKTOP_FILE="$APPS_DIR/beyne-at.desktop"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=Beyne At
Comment=Synapse-AG İkinci Beyin Akıllı Kaynak Yakalama
Exec=$WRAPPER %U
Terminal=false
Type=Application
Categories=Utility;Office;
MimeType=text/plain;text/uri-list;
EOF

chmod +x "$DESKTOP_FILE"

echo "[OK] Linux araçları kuruldu:"
echo "     -> CLI Wrapper: $WRAPPER"
echo "     -> Desktop Entry: $DESKTOP_FILE"
echo ""
echo "Kısayol ve Kullanım:"
echo "  * GNOME: Ayarlar > Klavye > Özel Kısayollar > Ekle (+)"
echo "    - Ad: Beyne At"
echo "    - Komut: $WRAPPER"
echo "    - Kısayol: Ctrl+Alt+B"
echo ""
echo "  * KDE Plasma:"
echo "    - Sistem Ayarları > Kısayollar > Özel Kısayol Ekle"
echo "    - Komut: $WRAPPER"
echo "    - Kısayol: Ctrl+Alt+B"
echo ""
echo "  * Hyprland / Sway:"
echo "    - bind = \$mainMod ALT, B, exec, $WRAPPER"
echo ""
echo "  * Obsidian Web Clipper:"
echo "    - https://obsidian.md/clipper eklentisini kurun."
echo "    - 000-Inbox/Yakala/beyne-at-web-clipper.json dosyasını içe aktarın."
echo "=========================================================="
