#!/usr/bin/env python3
"""
Antigravity 2.0 Beyin Doktoru (Diagnostics)
Checks files, hooks, scripts, git repository status and reports in a clear table.
"""
import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, get_version

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def check_file(path, label):
    p = Path(path)
    if p.exists():
        return "[OK] Hazir", "Yesil"
    return "[X] Eksik", "Kirmizi"

def run_git_check():
    try:
        res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        if res.returncode == 0:
            return "[OK] Git Aktif", "Yesil"
        return "[!] Git Baslatilmamis", "Sari"
    except Exception:
        return "[X] Git Bulunamadi", "Kirmizi"

def main():
    root = resolve_root()
    
    checks = [
        ("Kok Yonlendirici (GEMINI.md / beyin-antigravity.md)", root / "beyin-antigravity.md"),
        ("Versiyon Dosyasi (.beyin-version)", root / ".beyin-version"),
        ("Antigravity Kancalari (.agents/hooks.json)", root / ".agents" / "hooks.json"),
        ("Baglam Enjektoru (inject_context.py)", root / ".agents" / "scripts" / "inject_context.py"),
        ("Oturum Loglayici (flush_daily.py)", root / ".agents" / "scripts" / "flush_daily.py"),
        ("Bilgi Derleyici (compile_knowledge.py)", root / ".agents" / "scripts" / "compile_knowledge.py"),
        ("Obsidian Yapilandirmasi (.obsidian/)", root / ".obsidian" / "graph.json"),
        ("Sablon Kasasi (template/)", root / "template"),
    ]

    version = get_version(root)
    print("\n" + "=" * 65)
    print(f"     ANTIGRAVITY BEYIN DOKTORU RAPORU (v{version})")
    print("=" * 65)
    print(f"{'Bilesen':<48} | {'Durum':<12}")
    print("-" * 65)

    all_ok = True
    for name, path in checks:
        status, color = check_file(path, name)
        print(f"{name:<48} | {status:<12}")
        if "[X]" in status:
            all_ok = False

    git_status, _ = run_git_check()
    print(f"{'Git Surum Kontrolu':<48} | {git_status:<12}")
    print("=" * 65)

    if all_ok:
        print("[OK] Sistem sapasaglam! Tum hafiza kancalari ve dosyalar hazir.\n")
    else:
        print("[!] Bazi bilesenler eksik. Kurulumu 'beyin-antigravity.md' ile yapabilirsiniz.\n")

if __name__ == "__main__":
    main()
