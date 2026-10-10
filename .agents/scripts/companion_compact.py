#!/usr/bin/env python3
"""
Synapse-AG Companion Sıkıştırma ve Arşivleme Motoru (companion_compact.py)
Multi-process kilidi (.beyin-compact.lock) altında 850-Companion/ dosyalarını
aylık Arşiv/<Dosya>-YYYY-MM.md altına güvenle kopyalar ve sıkıştırır.
"""
import os
import sys
import re
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, safe_write

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def get_compact_lock(root):
    """companion klasöründe kalıcı .beyin-compact.lock dosya kilidi döndürür."""
    lock_path = root / "850-Companion" / ".beyin-compact.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    return lock_path

def archive_companion_file(file_path, archive_dir, dry_run=False):
    """Bir companion dosyasının tam metnini aylık Arşiv/<Dosya>-YYYY-MM.md altına yazar."""
    if not file_path.is_file():
        return False, "Dosya bulunamadı"

    content = file_path.read_text(encoding="utf-8")
    if not content.strip():
        return False, "Dosya boş"

    year_month = datetime.now().strftime("%Y-%m")
    archive_file = archive_dir / f"{file_path.stem}-{year_month}.md"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archive_entry = f"\n\n---\n## Arşiv Kaydı: {timestamp}\n\n{content}\n"
    
    if dry_run:
        return True, f"[DRY-RUN] {archive_file.name} içine yazılacaktı ({len(content)} karakter)"
    
    archive_dir.mkdir(parents=True, exist_ok=True)
    safe_write(archive_file, archive_entry, mode="a")
    return True, f"Arşivlendi -> {archive_file.name}"

def compact_file_content(file_path, max_lines=40, dry_run=False):
    """Dosyanın en güncel kısımlarını koruyarak başlıkları sıkıştırır."""
    if not file_path.is_file():
        return False, "Dosya bulunamadı"

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    if len(lines) <= max_lines:
        return False, f"Zaten sınır altında ({len(lines)}/{max_lines} satır)"

    header_lines = []
    body_lines = []
    in_frontmatter = False
    
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            header_lines.append(line)
            continue
        if in_frontmatter:
            header_lines.append(line)
            if line.strip() == "---":
                in_frontmatter = False
            continue
        if line.startswith("# ") and len(header_lines) < 5:
            header_lines.append(line)
            continue
        body_lines.append(line)

    keep_count = max_lines - len(header_lines) - 2
    if keep_count < 10:
        keep_count = 10
    
    trimmed_body = body_lines[-keep_count:]
    new_content = "\n".join(header_lines) + "\n\n> [!NOTE] Eski kayıtlar Arşiv klasörüne aktarıldı.\n\n" + "\n".join(trimmed_body) + "\n"
    
    if dry_run:
        return True, f"[DRY-RUN] {file_path.name}: {len(lines)} satırdan {len(new_content.splitlines())} satıra inecekti"

    safe_write(file_path, new_content, mode="w")
    return True, f"{file_path.name}: Sıkıştırıldı ({len(lines)} -> {len(new_content.splitlines())} satır)"

def run_compaction(root=None, dry_run=False):
    """Tüm Companion dosyalarını arşivler ve sıkıştırır."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    comp_dir = root / "850-Companion"
    if not comp_dir.exists():
        comp_dir = root / "🔮 850-Companion"
    
    archive_dir = root / "900-Archive" / "Companion"
    if not archive_dir.parent.exists():
        archive_dir = root / "Arşiv" / "Companion"

    lock_file = get_compact_lock(root)

    targets = [
        ("Last-Session.md", 45),
        ("Threads.md", 35),
        ("Kurallar.md", 50),
    ]

    results = []

    try:
        import portalocker
        lock_ctx = portalocker.Lock(str(lock_file), mode="w", timeout=10)
    except Exception:
        class DummyLock:
            def __enter__(self): return self
            def __exit__(self, *args): pass
        lock_ctx = DummyLock()

    with lock_ctx:
        for filename, max_l in targets:
            f_path = comp_dir / filename
            if f_path.is_file():
                # 1. Önce tam arşiv al
                arch_ok, arch_msg = archive_companion_file(f_path, archive_dir, dry_run=dry_run)
                # 2. Sonra sıkıştır
                comp_ok, comp_msg = compact_file_content(f_path, max_lines=max_l, dry_run=dry_run)
                results.append((filename, arch_msg, comp_msg))
            else:
                results.append((filename, "Mevcut değil", "Atlandı"))

    return results

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Companion Arşivleme ve Sıkıştırma Motoru")
    parser.add_argument("--dry-run", action="store_true", help="Yazma işlemi yapmadan simüle et")
    args = parser.parse_args()

    root = resolve_root()
    print(f"\n[Companion Compactor] Kök Dizin: {root}")
    if args.dry_run:
        print("[MOD] Dry-Run (Salt Okunur Simülasyon)")

    results = run_compaction(root, dry_run=args.dry_run)
    for fname, arch_m, comp_m in results:
        print(f" -> {fname:<18} | Arşiv: {arch_m:<35} | Sıkıştırma: {comp_m}")
    print("\n[OK] İşlem tamamlandı.\n")

if __name__ == "__main__":
    main()
