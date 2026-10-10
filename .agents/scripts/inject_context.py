#!/usr/bin/env python3
"""
Antigravity 2.0 PreInvocation Memory Injector (inject_context.py)
Reads companion state (Last-Session, Threads, Kurallar) and injects it into context.
Includes:
- 9.500 karakterlik katı bağlam bütçesi (Context Shield).
- Kurallar.md için akıllı kural budama (gerekçe/neden ayıklama).
- 'supersedes' ve emekli/arşivlenmiş durumlar filtresi.
"""
import sys
import json
import os
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root_from_payload

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

MAX_CONTEXT_CHARS = 9500

RETIRED_STATUSES = {
    "superseded", "retired", "archived", "deprecated",
    "obsolete", "replaced", "arşiv", "eski", "emekli", "geçersiz"
}

def is_retired_or_superseded(content):
    """Notun emekli, geçersiz veya superseded olup olmadığını inceler."""
    lower = content.lower()
    # 1. Frontmatter status kontrolü
    status_match = re.search(r"^status:\s*([a-zA-ZçğıöşüÇĞİÖŞÜ_-]+)", lower, re.MULTILINE)
    if status_match:
        val = status_match.group(1).strip()
        if any(val.startswith(ret) for ret in RETIRED_STATUSES):
            return True

    # 2. Frontmatter supersedes kontrolü
    if re.search(r"^superseded_by:\s*.+", lower, re.MULTILINE):
        return True

    # 3. Tags kontrolü
    tags_match = re.search(r"^tags:\s*\[(.*?)\]", lower, re.MULTILINE)
    if tags_match:
        tags = [t.strip().strip("'\"") for t in tags_match.group(1).split(",")]
        if any(t in RETIRED_STATUSES for t in tags):
            return True

    return False

def prune_rule_explanations(kurallar_content):
    """
    Kurallar.md içerisinden '**neden:**', '**gerekçe:**' ve uzun açıklama
    paragraflarını kırparak kural direktiflerini korur (AvenoxBeyin v3.7 standardı).
    """
    pruned_lines = []
    lines = kurallar_content.splitlines()
    for line in lines:
        stripped = line.strip()
        # Baştan başlayan neden/gerekçe satırlarını atla
        if re.search(r"^(\*\*|\*|\b)?(neden|gerekçe|sebebi|açıklama)\s*:", stripped, re.IGNORECASE):
            continue
        # Satır içi: "- Kural: ... **Neden:** ..." veya "... (neden: ...)"
        cleaned = re.sub(r"\s*(\*\*|\*|\b)(neden|gerekçe|sebebi|açıklama)\s*(\*\*|\*|\b)?\s*:.*$", "", line, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(neden:[^\)]+\)", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\(gerekçe:[^\)]+\)", "", cleaned, flags=re.IGNORECASE)
        pruned_lines.append(cleaned.strip())
    return "\n".join(pruned_lines)

def truncate_to_budget(sections, max_chars=MAX_CONTEXT_CHARS):
    """Toplam karakter sayısı max_chars sınırını aşmayacak şekilde bölümleri dengeler."""
    total_len = sum(len(s) for s in sections)
    if total_len <= max_chars:
        return sections

    # Öncelik sırası: Kimlik (1), Kurallar (4), Threads (3), Last-Session (2), Daily (6), KB (5)
    result = []
    for sec in sections:
        if len(sec) > 1500:
            lines = sec.splitlines()
            trimmed = "\n".join(lines[:25]) + "\n...[bağlam bütçesi için kısaltıldı]"
            result.append(trimmed)
        else:
            result.append(sec)

    current_len = sum(len(s) for s in result)
    if current_len > max_chars:
        final_sections = []
        rem = max_chars
        suffix = "\n...[kırpıldı]"
        suffix_len = len(suffix)
        for s in result:
            if len(s) <= rem:
                final_sections.append(s)
                rem -= len(s)
            else:
                take_len = max(0, rem - suffix_len)
                final_sections.append(s[:take_len] + suffix)
                break
        return final_sections

    return result

def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}

    root = resolve_root_from_payload(payload)

    mem_dir = root / "850-Companion"
    if not mem_dir.exists():
        mem_dir = root / "🔮 850-Companion"

    daily_dir = root / "daily"
    
    sections = []

    # 1. Identity & Core
    core_file = mem_dir / "Core.md"
    if core_file.is_file():
        try:
            core_content = core_file.read_text(encoding="utf-8").strip()
            if not is_retired_or_superseded(core_content):
                sections.append(f"[Hafıza: Kimlik & Amaç]\n{core_content}")
        except Exception:
            pass

    # 2. Last Session
    last_session_file = mem_dir / "Last-Session.md"
    if last_session_file.is_file():
        try:
            ls_content = last_session_file.read_text(encoding="utf-8").strip()
            if not is_retired_or_superseded(ls_content):
                lines = ls_content.splitlines()[:35]
                sections.append(f"[Hafıza: Son Oturum Özeti]\n" + "\n".join(lines))
        except Exception:
            pass

    # 3. Active Threads
    threads_file = mem_dir / "Threads.md"
    if threads_file.is_file():
        try:
            th_content = threads_file.read_text(encoding="utf-8").strip()
            if not is_retired_or_superseded(th_content):
                lines = th_content.splitlines()[:25]
                sections.append(f"[Hafıza: Aktif İş Parçacıkları]\n" + "\n".join(lines))
        except Exception:
            pass

    # 4. Kurallar (Rules) - Akıllı Budama Destekli
    kurallar_file = mem_dir / "Kurallar.md"
    if kurallar_file.is_file():
        try:
            kr_content = kurallar_file.read_text(encoding="utf-8").strip()
            if not is_retired_or_superseded(kr_content):
                # Bütçeyi aşarsa gerekçe/neden kısımlarını buda
                if len(kr_content) > 2000:
                    kr_content = prune_rule_explanations(kr_content)
                lines = kr_content.splitlines()[:40]
                sections.append(f"[Hafıza: Öğrenilen Kurallar]\n" + "\n".join(lines))
        except Exception:
            pass

    # 5. Knowledge Index
    kb_index = root / "knowledge" / "index.md"
    if kb_index.is_file():
        try:
            kb_content = kb_index.read_text(encoding="utf-8").strip()
            if not is_retired_or_superseded(kb_content):
                lines = kb_content.splitlines()[:20]
                sections.append(f"[Hafıza: Derlenmiş Bilgi İndeksi]\n" + "\n".join(lines))
        except Exception:
            pass

    # 6. Recent Daily Logs
    if daily_dir.is_dir():
        try:
            daily_files = sorted(daily_dir.glob("*.md"))
            if daily_files:
                latest_daily = daily_files[-1]
                daily_content = latest_daily.read_text(encoding="utf-8").strip()
                lines = daily_content.splitlines()[-25:] # Son 25 satır
                sections.append(f"[Hafıza: Son Oturumlar ({latest_daily.name})]\n" + "\n".join(lines))
        except Exception:
            pass

    if sections:
        safe_sections = truncate_to_budget(sections, max_chars=MAX_CONTEXT_CHARS)
        combined_message = "\n\n---\n\n".join(safe_sections)
        output = {
            "injectSteps": [
                {
                    "ephemeralMessage": f"🧠 [İkinci Beyin Durumu Yüklendi (Bağlam Bütçesi: {len(combined_message)}/{MAX_CONTEXT_CHARS} kr)]\n\n{combined_message}"
                }
            ]
        }
    else:
        output = {"injectSteps": []}

    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
