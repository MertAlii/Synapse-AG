#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synapse-AG / Alkan Second Brain - Full Migration & Backup Engine
Bilgisayar değiştirildiğinde veya tüm hafıza, projeler ve bilgi tabanını
taşımak/yedeklemek için tek tıkla çalışan arşivleme ve geri yükleme aracı.
"""

import os
import sys
import zipfile
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# Force UTF-8 stdout on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Paths to include in the portable brain package
INCLUDE_DIRS = [
    "🔮 850-Companion",
    "🏰 300-Projects",
    "🧠 500-Knowledge",
    "🎯 100-Command-Center",
    "daily",
    "knowledge",
    "000-Inbox",
    "Templates",
    ".agents",
    "visualizer"
]

INCLUDE_FILES = [
    "GEMINI.md",
    "Kurallar.md",
    "Last-Session.md",
    "Threads.md",
    "3D-Beyin.bat",
    "3D-Beyin.url",
    "README.md"
]

def export_brain(output_dir=None):
    root = Path(__file__).resolve().parent.parent.parent
    if not output_dir:
        output_dir = root
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Compile latest knowledge graph first
    try:
        compile_script = root / ".agents" / "scripts" / "compile_graph.py"
        if compile_script.exists():
            subprocess.run([sys.executable, str(compile_script)], check=False, cwd=str(root))
    except Exception as e:
        print(f"[!] Graph derleme atlandı: {e}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    zip_name = f"Alkan-Brain-Migration-Package_{timestamp}.zip"
    zip_path = output_dir / zip_name

    print(f"[*] Alkan İkinci Beyin Taşınabilir Paketi Hazırlanıyor...")
    print(f"    Hedef: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add root files
        for filename in INCLUDE_FILES:
            file_path = root / filename
            if file_path.exists():
                zipf.write(file_path, arcname=filename)
                print(f"  + Dosya eklendi: {filename}")

        # Add directories
        for dirname in INCLUDE_DIRS:
            dir_path = root / dirname
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        # Skip pycache / git internals
                        if "__pycache__" in str(file_path) or ".git" in str(file_path):
                            continue
                        arcname = file_path.relative_to(root).as_posix()
                        zipf.write(file_path, arcname=arcname)
                print(f"  + Klasör paketlendi: {dirname}")

        # Add a self-contained restore helper batch file inside zip
        restore_bat_content = """@echo off
echo ========================================================
echo   ALKAN IKINCI BEYIN - YENI BILGISAYAR KURULUMU
echo ========================================================
echo.
echo 1. Dosyalar mevcut konuma acildi.
echo 2. 3D Bilgi Grafigi derleniyor...
python .agents\\scripts\\compile_graph.py
echo.
echo [TAMAMLANDI] 3D-Beyin.bat dosyasini calistirarak baslayabilirsiniz!
pause
"""
        zipf.writestr("Yeni-Bilgisayara-Kur.bat", restore_bat_content)

    print(f"\n[OK] İkinci Beyin başarıyla paketlendi!")
    print(f"     Paket Konumu: {zip_path}")
    print(f"     Boyut: {zip_path.stat().st_size / 1024:.1f} KB")
    print(f"\n[?] Yeni bilgisayara taşırken:")
    print(f"    1. Bu .zip dosyasını yeni bilgisayarına kopyala ve bir klasöre çıkart.")
    print(f"    2. 'Yeni-Bilgisayara-Kur.bat' veya '3D-Beyin.bat' dosyasını çalıştır.")
    print(f"    3. Tüm hafıza, kurallar, projeler ve 3D görselleştirici anında hazır olacaktır.")
    return zip_path

def restore_brain(zip_file_path, target_dir=None):
    zip_path = Path(zip_file_path)
    if not zip_path.exists():
        print(f"[!] Hata: '{zip_file_path}' bulunamadı!")
        return False

    if not target_dir:
        target_dir = Path.cwd()
    else:
        target_dir = Path(target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"[*] Arşiv çıkartılıyor: {zip_path} -> {target_dir}")

    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(target_dir)

    # Re-compile graph
    try:
        compile_script = target_dir / ".agents" / "scripts" / "compile_graph.py"
        if compile_script.exists():
            subprocess.run([sys.executable, str(compile_script)], check=False, cwd=str(target_dir))
    except Exception as e:
        print(f"[!] Graph derleme hatası: {e}")

    print(f"[OK] İkinci beyin başarıyla geri yüklendi ve aktifleştirildi!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) > 2:
            restore_brain(sys.argv[2])
        else:
            print("Kullanım: python migrate_brain.py restore <backup.zip>")
    else:
        out_dir = sys.argv[1] if len(sys.argv) > 1 else None
        export_brain(out_dir)
