#!/usr/bin/env python3
"""
Antigravity 2.0 Beyin Doktoru Pro (doctor.py)
Checks files, hooks, scripts, git repository status, inbox aging,
git conflict markers, and superseded inferences.
"""
import os
import sys
import subprocess
import argparse
import json
import re
from datetime import datetime
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
        return "[OK] Hazır", True
    return "[X] Eksik", False

def run_git_check():
    try:
        res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        if res.returncode == 0:
            return "[OK] Git Aktif", True
        return "[!] Git Başlatılmamış", False
    except Exception:
        return "[X] Git Bulunamadı", False

def check_git_conflict_markers(root):
    """Kasadaki markdown dosyalarında <<<<<<<, =======, >>>>>>> işaretlerini tarar."""
    root = Path(root)
    conflicts = []
    
    # Taranacak uzantılar
    for p in root.rglob("*.md"):
        # .git ve sanal ortamları atla
        parts = p.parts
        if any(skip in parts for skip in [".git", "node_modules", ".venv", "venv", ".bak"]):
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
            if "<<<<<<<" in content and ">>>>>>>" in content:
                conflicts.append(p.relative_to(root))
        except Exception:
            pass

    return conflicts

def check_inbox_aging(root, max_days=7, max_items=30):
    """
    Inbox klasörlerindeki bekleyen notların yaşını ve sayısını denetler (AvenoxBeyin v3.9 standardı).
    """
    root = Path(root)
    inbox_dirs = [
        root / "000-Inbox",
        root / "📥 000-Inbox",
    ]
    
    pending_items = []
    now = datetime.now()

    for ib in inbox_dirs:
        if not ib.exists():
            continue
        for p in ib.rglob("*.md"):
            # .ham veya gizli klasörleri atla
            if ".ham" in p.parts:
                continue
            try:
                mtime = datetime.fromtimestamp(p.stat().st_mtime)
                age_days = (now - mtime).days
                pending_items.append({
                    "path": str(p.relative_to(root)),
                    "filename": p.name,
                    "age_days": age_days,
                    "mtime": mtime.strftime("%Y-%m-%d")
                })
            except Exception:
                pass

    total = len(pending_items)
    old_items = [item for item in pending_items if item["age_days"] >= max_days]
    
    is_warning = (total > max_items) or (len(old_items) > 0)
    return {
        "total_items": total,
        "old_items_count": len(old_items),
        "old_items": old_items,
        "all_items": pending_items,
        "is_warning": is_warning,
        "max_days": max_days,
        "max_items": max_items,
    }

def check_supersedes_and_inferences(root):
    """
    Kasadaki superseded / retired etiketli veya reddedilmiş çıkarımları denetler.
    """
    root = Path(root)
    superseded_notes = []
    retired_tags = {"superseded", "retired", "archived", "deprecated", "arşiv", "eski", "emekli", "geçersiz"}

    for p in root.rglob("*.md"):
        parts = p.parts
        if any(skip in parts for skip in [".git", "node_modules", "900-Archive", "Arşiv", ".bak"]):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")[:1000]
            status_match = re.search(r"^status:\s*([a-zA-ZçğıöşüÇĞİÖŞÜ_-]+)", text.lower(), re.MULTILINE)
            if status_match and any(status_match.group(1).startswith(r) for r in retired_tags):
                superseded_notes.append(str(p.relative_to(root)))
        except Exception:
            pass

    return superseded_notes

def main():
    parser = argparse.ArgumentParser(description="Antigravity Synapse-AG Beyin Doktoru Pro")
    parser.add_argument("--inbox-report", action="store_true", help="Detaylı gelen kutusu yaşlanma raporu sun")
    parser.add_argument("--full", action="store_true", help="Tüm gelişmiş denetimleri çalıştır")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında ver")
    parser.add_argument("--inbox-max-days", type=int, default=7, help="Maksimum inbox bekleme günü (varsayılan: 7)")
    parser.add_argument("--inbox-max-items", type=int, default=30, help="Maksimum inbox bekleme öğesi (varsayılan: 30)")
    args = parser.parse_args()

    root = resolve_root()
    version = get_version(root)

    core_checks = [
        ("Kök Yönlendirici (GEMINI.md / beyin-antigravity.md)", root / "beyin-antigravity.md"),
        ("Versiyon Dosyası (.beyin-version)", root / ".beyin-version"),
        ("Antigravity Kancaları (.agents/hooks.json)", root / ".agents" / "hooks.json"),
        ("Bağlam Enjektörü (inject_context.py)", root / ".agents" / "scripts" / "inject_context.py"),
        ("Oturum Loglayıcı (flush_daily.py)", root / ".agents" / "scripts" / "flush_daily.py"),
        ("Bilgi Derleyici (compile_knowledge.py)", root / ".agents" / "scripts" / "compile_knowledge.py"),
        ("Companion Sıkıştırıcı (companion_compact.py)", root / ".agents" / "scripts" / "companion_compact.py"),
        ("Akıllı Yakalama Motoru (yakala.py)", root / ".agents" / "scripts" / "yakala.py"),
        ("BM25 Türkçe Arama (search_bm25.py)", root / ".agents" / "scripts" / "search_bm25.py"),
        ("Nedensellik RAG (causal_rag.py)", root / ".agents" / "scripts" / "causal_rag.py"),
        ("Bilişsel Hafıza (cognitive_memory.py)", root / ".agents" / "scripts" / "cognitive_memory.py"),
        ("Şeytanın Avukatı (adversarial_rag.py)", root / ".agents" / "scripts" / "adversarial_rag.py"),
        ("Synapse TUI (tui.py)", root / ".agents" / "scripts" / "tui.py"),
        ("Yan Panel Uzantısı (synapse-sidecar)", root / "plugins" / "synapse-sidecar" / "plugin.json"),
        ("Obsidian Yapılandırması (.obsidian/)", root / ".obsidian" / "graph.json"),
        ("Şablon Kasası (Templates/)", root / "Templates"),
    ]

    all_ok = True
    check_results = []
    for name, path in core_checks:
        status, ok = check_file(path, name)
        check_results.append((name, status))
        if not ok:
            all_ok = False

    git_status, git_ok = run_git_check()
    if not git_ok:
        all_ok = False

    # Gelişmiş denetimler
    conflicts = check_git_conflict_markers(root)
    inbox_data = check_inbox_aging(root, max_days=args.inbox_max_days, max_items=args.inbox_max_items)
    superseded_list = check_supersedes_and_inferences(root)

    if args.json:
        report = {
            "version": version,
            "root": str(root),
            "all_ok": all_ok and (len(conflicts) == 0) and (not inbox_data["is_warning"]),
            "core_checks": {n: s for n, s in check_results},
            "git_status": git_status,
            "conflicts": [str(c) for c in conflicts],
            "inbox_report": inbox_data,
            "superseded_count": len(superseded_list),
            "superseded_notes": superseded_list,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print("\n" + "=" * 70)
    print(f"        ANTIGRAVITY BEYİN DOKTORU PRO RAPORU (v{version})")
    print("=" * 70)
    print(f"{'Bileşen':<52} | {'Durum':<14}")
    print("-" * 70)

    for name, status in check_results:
        print(f"{name:<52} | {status:<14}")

    print(f"{'Git Sürüm Kontrolü':<52} | {git_status:<14}")
    print("-" * 70)

    # Git çakışma raporu
    if conflicts:
        print(f"{'Git Çakışma İşaretleri (<<<<<<<, >>>>>>>)':<52} | [X] {len(conflicts)} dosya!")
        for c in conflicts[:5]:
            print(f"   -> Bozuk dosya: {c}")
        all_ok = False
    else:
        print(f"{'Git Çakışma İşaretleri':<52} | [OK] Temiz")

    # Inbox raporu
    ib_status = f"{inbox_data['total_items']} öğe ({inbox_data['old_items_count']} eski)"
    if inbox_data["is_warning"]:
        print(f"{'Gelen Kutusu (Inbox) Yaşlanma':<52} | [!] {ib_status}")
    else:
        print(f"{'Gelen Kutusu (Inbox) Yaşlanma':<52} | [OK] {ib_status}")

    # Supersedes raporu
    print(f"{'Emekli / Superseded Not Filtresi':<52} | [OK] {len(superseded_list)} not tespit edildi")
    print("=" * 70)

    if args.inbox_report or args.full:
        print("\n📥 DETAYLI GELEN KUTUSU (INBOX) ANALİZİ:")
        if inbox_data["all_items"]:
            for item in sorted(inbox_data["all_items"], key=lambda x: x["age_days"], reverse=True)[:10]:
                warn = " ⚠️ [ESKİ]" if item["age_days"] >= args.inbox_max_days else ""
                print(f" - {item['filename']} ({item['age_days']} gündür bekliyor, {item['mtime']}){warn}")
            if len(inbox_data["all_items"]) > 10:
                print(f"   ... ve {len(inbox_data['all_items']) - 10} adet daha")
        else:
            print(" - Gelen kutusu tertemiz, bekleyen not yok!")
        print("-" * 70)

    if all_ok and not conflicts:
        print("[OK] Sistem sapasağlam! Tüm kancalar, güvenlik kalkanları ve dosyalar hazır.\n")
    else:
        print("[!] Bazı bileşenler veya denetimler dikkat gerektiriyor.\n")

if __name__ == "__main__":
    main()
