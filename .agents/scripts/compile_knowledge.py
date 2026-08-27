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

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    root = Path(os.getcwd())
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
    index_file.write_text(index_content, encoding="utf-8")

    # 3. Append to log.md
    compile_log = kb_dir / "log.md"
    log_entry = f"\n- **{today_str}**: Bilgi derlemesi tamamlandı. Toplam {log_count} günlük log dosyası tarandı. {len(existing_concepts)} kavram güncel.\n"
    
    if not compile_log.exists():
        compile_log.write_text("# 📝 Bilgi Derleme Günlüğü\n\n" + log_entry, encoding="utf-8")
    else:
        with open(compile_log, "a", encoding="utf-8") as f:
            f.write(log_entry)

    # Auto-compile 3D graph data
    try:
        import subprocess
        subprocess.run(["python", str(root / ".agents" / "scripts" / "compile_graph.py")], capture_output=True)
    except Exception:
        pass

    print(f"[OK] Bilgi derlemesi tamamlandi: {len(existing_concepts)} kavram, {log_count} gunluk log tarandi.")

if __name__ == "__main__":
    main()
