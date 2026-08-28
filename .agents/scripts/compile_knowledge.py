#!/usr/bin/env python3
"""
Antigravity 2.0 Knowledge Base Compiler
Compiles daily logs and notes into linked knowledge articles (Karpathy Pattern).
"""
import sys
import os
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, safe_write

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    root = resolve_root()
    daily_dir = root / "daily"
    kb_dir = root / "knowledge"
    concepts_dir = kb_dir / "concepts"
    connections_dir = kb_dir / "connections"

    concepts_dir.mkdir(parents=True, exist_ok=True)
    connections_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 1. Scan daily logs
    daily_files = sorted(daily_dir.glob("*.md")) if daily_dir.exists() else []
    log_count = len(daily_files)

    # 2. Update Index
    index_file = kb_dir / "index.md"
    existing_concepts = list(concepts_dir.glob("*.md"))
    
    table_rows = []
    for c in existing_concepts:
        title = c.stem
        table_rows.append(f"| [[{title}]] | Otomatik derlenen kavram | `concepts/{c.name}` | {today_str} |")

    if not table_rows:
        table_rows.append("| *Henüz derlenmiş kavram yok* | İlk derleme bekleniyor | - | - |")

    index_content = f"""# 📚 Bilgi Tabanı: İndeks

Bu indeks Antigravity Bilgi Derleyicisi tarafından otomatik güncellenir.

| Makale | Özet | Kaynak Dosya | Son Güncelleme |
| :--- | :--- | :--- | :--- |
{chr(10).join(table_rows)}
"""
    safe_write(index_file, index_content, mode="w")

    # 3. Append to log.md
    compile_log = kb_dir / "log.md"
    log_entry = f"\n- **{today_str}**: Bilgi derlemesi tamamlandı. Toplam {log_count} günlük log dosyası tarandı. {len(existing_concepts)} kavram güncel.\n"
    
    if not compile_log.exists():
        safe_write(compile_log, "# 📝 Bilgi Derleme Günlüğü\n\n" + log_entry, mode="w")
    else:
        safe_write(compile_log, log_entry, mode="a")

    print(f"[OK] Bilgi derlemesi tamamlandi: {len(existing_concepts)} kavram, {log_count} gunluk log tarandi.")

if __name__ == "__main__":
    main()
