#!/usr/bin/env python3
"""
Antigravity 2.0 Daily Session Flusher
Summarizes the finished session and appends it to daily/YYYY-MM-DD.md.
"""
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# _resolve_root modülünü import et
sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root_from_payload, safe_write, get_version

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def parse_transcript(transcript_path):
    """Extract key conversation points from transcript.jsonl"""
    if not transcript_path or not os.path.exists(transcript_path):
        return []
    
    entries = []
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    step_type = data.get("type", "")
                    content = data.get("content", "")
                    if step_type in ("USER_INPUT", "PLANNER_RESPONSE") and content:
                        entries.append({
                            "type": step_type,
                            "content": content[:300].strip()
                        })
                except Exception:
                    continue
    except Exception:
        pass
    return entries

def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}

    root = resolve_root_from_payload(payload)

    daily_dir = root / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)

    today_str = datetime.now().strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")
    daily_file = daily_dir / f"{today_str}.md"

    # Transcript extraction
    transcript_path = payload.get("transcriptPath", "")
    entries = parse_transcript(transcript_path)

    summary_bullets = []
    if entries:
        for idx, entry in enumerate(entries[-6:], 1):
            speaker = "Kullanıcı" if entry["type"] == "USER_INPUT" else "Asistan"
            snippet = entry["content"].replace("\n", " ")
            if len(snippet) > 120:
                snippet = snippet[:117] + "..."
            summary_bullets.append(f"- **{speaker}:** {snippet}")
    else:
        summary_bullets.append(f"- *Oturum {now_time}'de tamamlandı.* (Transcript verisi alınamadı)")

    session_block = f"""
### Oturum: {now_time}
{chr(10).join(summary_bullets)}
"""

    if not daily_file.exists():
        header = f"""---
title: {today_str} Günlük Oturum Logları
date: {today_str}
type: daily-log
---
# 📅 {today_str} Günlük Loglar

"""
        safe_write(daily_file, header + session_block.strip() + "\n", mode="w")
    else:
        safe_write(daily_file, "\n" + session_block.strip() + "\n", mode="a")

    # Stop hook output
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
