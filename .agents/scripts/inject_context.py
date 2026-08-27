#!/usr/bin/env python3
"""
Antigravity 2.0 PreInvocation Memory Injector
Reads companion state (Last-Session, Threads, Kurallar) and injects it into context.
"""
import sys
import json
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}

    # Workspace directory
    workspace_paths = payload.get("workspacePaths", [])
    if workspace_paths:
        root = Path(workspace_paths[0])
    else:
        root = Path(os.getcwd())

    mem_dir = root / "🔮 850-Companion"
    
    sections = []

    # 1. Identity & Core
    core_file = mem_dir / "Core.md"
    if core_file.is_file():
        try:
            core_content = core_file.read_text(encoding="utf-8").strip()
            sections.append(f"[Hafıza: Kimlik & Amaç]\n{core_content}")
        except Exception:
            pass

    # 2. Last Session
    last_session_file = mem_dir / "Last-Session.md"
    if last_session_file.is_file():
        try:
            ls_content = last_session_file.read_text(encoding="utf-8").strip()
            lines = ls_content.splitlines()[:40]
            sections.append(f"[Hafıza: Son Oturum Özeti]\n" + "\n".join(lines))
        except Exception:
            pass

    # 3. Active Threads
    threads_file = mem_dir / "Threads.md"
    if threads_file.is_file():
        try:
            th_content = threads_file.read_text(encoding="utf-8").strip()
            lines = th_content.splitlines()[:25]
            sections.append(f"[Hafıza: Aktif İş Parçacıkları]\n" + "\n".join(lines))
        except Exception:
            pass

    # 4. Kurallar (Rules)
    kurallar_file = mem_dir / "Kurallar.md"
    if kurallar_file.is_file():
        try:
            kr_content = kurallar_file.read_text(encoding="utf-8").strip()
            lines = kr_content.splitlines()[:30]
            sections.append(f"[Hafıza: Öğrenilen Kurallar]\n" + "\n".join(lines))
        except Exception:
            pass

    # 5. Knowledge Index
    kb_index = root / "knowledge" / "index.md"
    if kb_index.is_file():
        try:
            kb_content = kb_index.read_text(encoding="utf-8").strip()
            lines = kb_content.splitlines()[:20]
            sections.append(f"[Hafıza: Derlenmiş Bilgi İndeksi]\n" + "\n".join(lines))
        except Exception:
            pass

    if sections:
        combined_message = "\n\n---\n\n".join(sections)
        output = {
            "injectSteps": [
                {
                    "ephemeralMessage": f"🧠 [İkinci Beyin Durumu Yüklendi]\n\n{combined_message}"
                }
            ]
        }
    else:
        output = {"injectSteps": []}

    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
