#!/usr/bin/env python3
"""
Synapse-AG Şeytanın Avukatı RAG (adversarial_rag.py)
--------------------------------------------------
Mimari ve teknolojik kararlarda körü körüne onaylamak yerine,
kasanın geçmiş post-mortem, hata kütüğü ve vazgeçiş gerekçelerini
karşıt argüman olarak sunar.
"""
import os
import sys
import re
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root
from search_bm25 import tokenize_and_stem
from causal_rag import search_causal_trajectories

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Sık karşılaşılan teknolojik tuzaklar ve bilinen karşıt argümanlar
KNOWN_PITFALLS = {
    "sqlite": {
        "warning": "Yüksek eşzamanlı (concurrent) yazma işlemlerinde SQLite 'database is locked' timeout hatası verebilir. Çoklu subagent veya arka plan worker'ları yoğunsa WAL modu (Write-Ahead Logging) veya PostgreSQL düşünülmelidir.",
        "tags": ["sqlite", "concurrency", "lock", "database"]
    },
    "microservice": {
        "warning": "Erken aşamada mikroservis mimarisine geçmek; ağ gecikmesi, dağıtık işlem (distributed transaction) karmaşıklığı ve deployment yükü getirir. Başlangıçta modüler monolit tercih edilmelidir.",
        "tags": ["microservice", "monolith", "distributed", "architecture"]
    },
    "string replace": {
        "warning": "Teknik çevirilerde veya kod dönüştürmede yüzeysel string replace kod bloklarını bozar ve bağlamı yitirir (Bkz: Lessons.md DERS-004). Tam AST veya kavramsal ayrıştırma kullanılmalıdır.",
        "tags": ["replace", "regex", "ast", "parsing"]
    },
    "spa": {
        "warning": "IIS veya Nginx üzerinde SPA dağıtırken sunucu tarafı URL Rewrite (index.html fallback) kuralı unutulursa sayfa yenilemede 404 alınır (Bkz: Lessons.md DERS-003).",
        "tags": ["spa", "iis", "nginx", "routing", "rewrite"]
    },
    "state": {
        "warning": "React form veya async submit butonlarında state bildirimi eksik kalırsa ReferenceError ile tüm component ağacı çöker (Bkz: Lessons.md DERS-005). ErrorBoundary kök seviyede zorunludur.",
        "tags": ["react", "state", "errorboundary", "crash"]
    }
}

def evaluate_adversarial_perspective(proposal_text, root=None):
    """
    Kullanıcının önerdiği mimari veya teknoloji kararını geçmiş hatalar ve anti-pattern'larla test eder.
    """
    if root is None:
        root = resolve_root()
    root = Path(root)

    findings = []
    tokens = set(tokenize_and_stem(proposal_text.lower()))
    norm_text = proposal_text.lower()

    # 1. Bilinen kritik tuzaklar kontrolü
    for key, data in KNOWN_PITFALLS.items():
        if key in norm_text or any(t in tokens for t in data["tags"]):
            findings.append({
                "type": "known_anti_pattern",
                "title": f"Teknoloji Riski: {key.upper()}",
                "counter_argument": data["warning"],
                "source": "Synapse-AG Architecture Guardrails"
            })

    # 2. Kasadaki Lessons.md ve nedensellik zincirlerini ara
    causal_matches = search_causal_trajectories(proposal_text, root=root, top_k=2)
    for match in causal_matches:
        findings.append({
            "type": "historical_lesson",
            "title": f"Geçmiş Deneyim: {match['id']} - {match['title']}",
            "counter_argument": f"⚠️ Karşılaşılan Sorun: {match['problem']}\n   💥 Neden Patladı: {match['failed_attempts']}\n   ✅ Çözüm: {match['working_solution']}",
            "source": match["source_file"]
        })

    return findings

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Şeytanın Avukatı RAG")
    parser.add_argument("proposal", help="Değerlendirilecek mimari, kütüphane veya tasarım kararı")
    parser.add_argument("--json", action="store_true", help="JSON formatında döndür")
    args = parser.parse_args()

    root = resolve_root()
    findings = evaluate_adversarial_perspective(args.proposal, root=root)

    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
        return

    print("\n=======================================================================")
    print("      😈 ŞEYTANIN AVUKATI RAG (CONTRASTIVE RETRIEVAL RAPORU)")
    print("=======================================================================")
    print(f"Öneri / Karar : \"{args.proposal}\"\n")

    if not findings:
        print("[OK] Bu karar için kasada kayıtlı geçmiş bir hata veya bilinen kritik tuzak tespit edilmedi.")
        print("     Karar ilerletilebilir, ancak yan etkileri test etmeyi unutmayın.")
    else:
        print(f"[!] DİKKAT: Bu kararla ilgili {len(findings)} potansiyel risk ve geçmiş tecrübe bulundu:\n")
        for idx, f in enumerate(findings, 1):
            print(f"[{idx}] {f['title']}")
            print(f"    {f['counter_argument']}")
            print(f"    📄 Referans: [[{f['source']}]]\n")

    print("=======================================================================\n")

if __name__ == "__main__":
    main()
