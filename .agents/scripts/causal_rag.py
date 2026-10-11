#!/usr/bin/env python3
"""
Synapse-AG Nedensellik Zinciri & Karar Ağacı RAG (causal_rag.py)
--------------------------------------------------------------
RAG'ın yalnızca "ne yapıldığını" değil; "neden öyle yapıldığını",
"nelerin denenip patladığını" ve "nihai çalışan çözümü" (Causal Trajectory)
getirmesini sağlar.
"""
import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, safe_write
from search_bm25 import tokenize_and_stem

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def parse_lesson_blocks(content, filepath="500-Knowledge/Lessons.md"):
    """Lessons.md veya benzeri dosyalardan nedensellik bloklarını ayrıştırır."""
    trajectories = []
    # [DERS-XXX] başlıklarına göre böl
    pattern = r"###\s*\[(.*?)\]\s*(.*?)\n(.*?)(?=\n###|\Z)"
    matches = re.findall(pattern, content, flags=re.DOTALL)

    for mid, title, body in matches:
        problem = ""
        root_cause = ""
        failed_attempts = ""
        action = ""
        rule = ""
        tags = []

        # Satırları veya alt başlıkları ayrıştır
        p_match = re.search(r"-\s*\*\*Karşılaşılan Sorun[^:]*:\*\*\s*(.*?)(?=\n-|\Z)", body, re.DOTALL)
        if p_match:
            problem = p_match.group(1).strip()

        rc_match = re.search(r"-\s*\*\*Kök Neden[^:]*:\*\*\s*(.*?)(?=\n-|\Z)", body, re.DOTALL)
        if rc_match:
            root_cause = rc_match.group(1).strip()

        act_match = re.search(r"-\s*\*\*Alınan Aksiyon:\*\*\s*(.*?)(?=\n-|\Z)", body, re.DOTALL)
        if act_match:
            action = act_match.group(1).strip()

        rule_match = re.search(r"-\s*\*\*[^:]*Kural:\*\*\s*(.*?)(?=\n-|\Z)", body, re.DOTALL)
        if rule_match:
            rule = rule_match.group(1).strip()

        tag_match = re.search(r"-\s*\*\*Etiketler:\*\*\s*(.*?)(?=\n-|\Z)", body, re.DOTALL)
        if tag_match:
            tags = re.findall(r"#([\w-]+)", tag_match.group(1))

        # Başarısız denemeleri kök neden ve aksiyondan filtrele
        if "denendi" in root_cause.lower() or "hata" in root_cause.lower():
            failed_attempts = root_cause
        else:
            failed_attempts = f"Kök neden: {root_cause}"

        trajectories.append({
            "id": mid.strip(),
            "title": title.strip(),
            "problem": problem or title.strip(),
            "root_cause": root_cause,
            "failed_attempts": failed_attempts,
            "working_solution": action or "Belirtilmemiş",
            "rule": rule,
            "tags": tags,
            "source_file": str(filepath).replace("\\", "/")
        })

    return trajectories

def parse_decision_blocks(content, filepath="Templates/Decision.md"):
    """Karar dosyalarından (ADR / Decision) nedensellik zincirini ayrıştırır."""
    trajectories = []
    # Başlık
    title_m = re.search(r"^#\s*(.*?)$", content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else Path(filepath).stem

    # Bağlam & Sorun
    ctx_m = re.search(r"##\s*🎯\s*Bağlam ve Sorun\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    context = ctx_m.group(1).strip() if ctx_m else ""

    # Değerlendirilen / Reddedilen Seçenekler
    alt_m = re.search(r"##\s*⚖️\s*Değerlendirilen Seçenekler\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    alternatives = alt_m.group(1).strip() if alt_m else ""

    # Nihai Karar
    dec_m = re.search(r"##\s*✅\s*Alınan Karar\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    decision = dec_m.group(1).strip() if dec_m else ""

    if context or decision:
        trajectories.append({
            "id": Path(filepath).stem,
            "title": title,
            "problem": context,
            "root_cause": "Tasarım & Mimari Seçimi",
            "failed_attempts": alternatives or "Alternatifler elendi",
            "working_solution": decision,
            "rule": "",
            "tags": ["decision", "adr", "architecture"],
            "source_file": str(filepath).replace("\\", "/")
        })

    return trajectories

def build_causal_index(root=None):
    """Kasadaki Lessons.md, Decision kayıtları ve daily loglardan nedensellik indeksini çıkarır."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    all_trajectories = []

    # 1. Lessons.md
    lessons_path = root / "500-Knowledge" / "Lessons.md"
    if lessons_path.exists():
        content = lessons_path.read_text(encoding="utf-8", errors="replace")
        all_trajectories.extend(parse_lesson_blocks(content, lessons_path.relative_to(root)))

    # 2. Decision belgeleri
    for dpath in root.rglob("*.md"):
        parts = dpath.parts
        if any(skip in parts for skip in [".git", "node_modules", ".venv", "venv", ".bak", ".ham"]):
            continue
        if "decision" in dpath.name.lower() or "karar" in dpath.name.lower():
            try:
                txt = dpath.read_text(encoding="utf-8", errors="replace")
                all_trajectories.extend(parse_decision_blocks(txt, dpath.relative_to(root)))
            except Exception:
                pass

    # Kaydet
    state_dir = root / ".agents" / "scripts" / ".state"
    state_dir.mkdir(parents=True, exist_ok=True)
    index_file = state_dir / "causal_index.json"
    safe_write(index_file, json.dumps(all_trajectories, ensure_ascii=False, indent=2), mode="w")
    return all_trajectories

def search_causal_trajectories(query, root=None, top_k=3):
    """
    Kullanıcının karşılaştığı hata veya kararı sorgulayarak geçmiş nedensellik zincirini getirir.
    """
    if root is None:
        root = resolve_root()
    root = Path(root)

    state_dir = root / ".agents" / "scripts" / ".state"
    index_file = state_dir / "causal_index.json"

    if index_file.exists():
        try:
            trajectories = json.loads(index_file.read_text(encoding="utf-8"))
        except Exception:
            trajectories = build_causal_index(root)
    else:
        trajectories = build_causal_index(root)

    q_tokens = set(tokenize_and_stem(query))
    if not q_tokens:
        return []

    scored = []
    for item in trajectories:
        text_corpus = f"{item['title']} {item['problem']} {item['root_cause']} {item['failed_attempts']} {item['working_solution']} {' '.join(item['tags'])}"
        doc_tokens = set(tokenize_and_stem(text_corpus))

        overlap = q_tokens.intersection(doc_tokens)
        if overlap:
            score = len(overlap) / float(len(q_tokens) + 1)
            # Etiket veya başlık eşleşmelerine ek ağırlık ver
            tag_overlap = q_tokens.intersection(set(item['tags']))
            score += len(tag_overlap) * 0.3
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for score, item in scored[:top_k]]

def format_causal_result(item):
    """Nedensellik kartını okunabilir biçimlendirir."""
    lines = [
        f"💡 [Nedensellik Zinciri & Trajectory: {item['id']}] - {item['title']}",
        f"   🎯 Karşılaşılan Sorun : {item['problem'][:200]}",
        f"   ⚠️ Neler Denendi / Neden Patladı: {item['failed_attempts'][:200]}",
        f"   ✅ Çalışan Kesin Çözüm: {item['working_solution'][:300]}"
    ]
    if item.get("rule"):
        lines.append(f"   🔮 Kazanılan İlke/Kural: {item['rule']}")
    lines.append(f"   📄 Kaynak: [[{item['source_file']}]]")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Nedensellik Zinciri & Karar Ağacı RAG")
    parser.add_argument("query", nargs="?", default="", help="Hata, problem veya karar sorgusu")
    parser.add_argument("--index", action="store_true", help="Nedensellik indeksini yeniden oluştur")
    parser.add_argument("--json", action="store_true", help="Sonuçları JSON formatında döndür")
    args = parser.parse_args()

    root = resolve_root()

    if args.index or not args.query:
        trajectories = build_causal_index(root)
        print(f"\n[OK] Nedensellik indeksi oluşturuldu: {len(trajectories)} adet yörünge/karar indekslendi.\n")
        if not args.query:
            return

    results = search_causal_trajectories(args.query, root=root)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if not results:
        print(f"\n[i] '{args.query}' için geçmişte kayıtlı bir hata yörüngesi veya patlayan deneme bulunamadı.\n")
        return

    print(f"\n🔍 '{args.query}' ile İlgili Geçmiş Nedensellik ve Çözüm Zincirleri ({len(results)} Kayıt):\n")
    for r in results:
        print(format_causal_result(r))
        print("-" * 70)
    print()

if __name__ == "__main__":
    main()
