#!/usr/bin/env python3
"""
Synapse-AG Akıllı BM25 & Türkçe Morfolojik Arama Motoru (search_bm25.py)
Okapi BM25 skorlaması, Türkçe ünsüz yumuşaması normalizasyonu,
Obsidian [[Wikilinks]] ve başlık ağırlıklandırması içerir.
"""
import os
import sys
import math
import re
import argparse
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Sık kullanılan Türkçe çekim ekleri (uzundan kısaya sıralı)
TURKISH_SUFFIXES = [
    "lerinden", "larından", "lerindeki", "larındaki",
    "lerinde", "larında", "lerin", "ların", "lerden", "lardan",
    "leriyle", "larıyla", "lerinize", "larınıza",
    "daki", "deki", "taki", "teki",
    "dan", "den", "tan", "ten",
    "lar", "ler", "nın", "nin", "nun", "nün",
    "mız", "miz", "muz", "müz", "nız", "niz",
    "da", "de", "ta", "te",
    "ya", "ye", "yı", "yi", "yu", "yü",
    "in", "ın", "un", "ün",
    "a", "e", "ı", "i", "u", "ü"
]

# Ünsüz yumuşaması harf dönüşüm tablosu (b->p, c->ç, d->t, ğ->k, g->k)
CONSONANT_SOFTENING = {
    "b": "p",
    "c": "ç",
    "d": "t",
    "ğ": "k",
    "g": "k"
}

def normalize_turkish_token(token):
    """
    Türkçe tokeni normalize eder: küçük harfe çevirir,
    çekim eklerini budar ve ünsüz yumuşamasını orijinal köke eşitler.
    Örnek: 'kitabı' -> 'kitap', 'örneği' -> 'örnek', 'renkleri' -> 'renk'
    """
    token = token.strip().lower()
    # Noktalama temizliği
    token = re.sub(r"^[^\w]+|[^\w]+$", "", token)
    if len(token) <= 2:
        return token

    # Çekim eklerini buda
    stem = token
    for suffix in TURKISH_SUFFIXES:
        if stem.endswith(suffix) and len(stem) - len(suffix) >= 3:
            stem = stem[:-len(suffix)]
            break

    # Ünsüz yumuşaması kök düzeltmesi (Son harf b,c,d,ğ,g ise p,ç,t,k'ye çevir)
    if stem and stem[-1] in CONSONANT_SOFTENING:
        stem = stem[:-1] + CONSONANT_SOFTENING[stem[-1]]

    return stem

def tokenize_and_stem(text):
    """Metni kelimelere böler ve köklerine ayırır."""
    raw_tokens = re.findall(r"\b[a-zA-ZçğıöşüÇĞİÖŞÜ0-9_-]+\b", text)
    return [normalize_turkish_token(t) for t in raw_tokens if len(t) > 1]

class BM25SearchEngine:
    def __init__(self, root, k1=1.5, b=0.75):
        self.root = Path(root)
        self.k1 = k1
        self.b = b
        self.documents = [] # list of dict: {path, title, wikilinks, tokens, doc_len, raw_text}
        self.doc_freqs = Counter()
        self.avg_doc_len = 0.0
        self.total_docs = 0
        self._index_documents()

    def _index_documents(self):
        """Kasadaki tüm aktif markdown dosyalarını indeksler."""
        skip_folders = {".git", "node_modules", ".venv", "venv", ".bak", "Arşiv", "900-Archive"}
        all_tokens_count = 0

        for p in self.root.rglob("*.md"):
            if any(part in skip_folders for part in p.parts):
                continue
            # .ham gizli klasörünü atla
            if ".ham" in p.parts:
                continue

            try:
                raw_text = p.read_text(encoding="utf-8", errors="ignore")
                
                # Emekli / superseded not kontrolü
                lower_text = raw_text.lower()
                if "status: superseded" in lower_text or "status: retired" in lower_text:
                    continue

                # Wikilinkleri ve başlığı çıkar
                title = p.stem
                wikilinks = re.findall(r"\[\[(.*?)\]\]", raw_text)
                
                # Başlık ve wikilinklere öncelik vermek için metne ağırlıklı ekle
                weighted_text = f"{title} {title} " + " ".join(wikilinks) + " " + raw_text

                tokens = tokenize_and_stem(weighted_text)
                doc_len = len(tokens)
                if doc_len == 0:
                    continue

                all_tokens_count += doc_len
                self.documents.append({
                    "path": p,
                    "rel_path": str(p.relative_to(self.root)),
                    "title": title,
                    "wikilinks": wikilinks,
                    "tokens": tokens,
                    "doc_len": doc_len,
                    "raw_text": raw_text
                })

                # Belge frekansı
                unique_tokens = set(tokens)
                for t in unique_tokens:
                    self.doc_freqs[t] += 1

            except Exception:
                pass

        self.total_docs = len(self.documents)
        if self.total_docs > 0:
            self.avg_doc_len = all_tokens_count / self.total_docs

    def search(self, query, top_k=5):
        """BM25 algoritması ile sorguyu puanlar ve en alakalı sonuçları döndürür."""
        query_tokens = [normalize_turkish_token(t) for t in query.split() if t.strip()]
        if not query_tokens or self.total_docs == 0:
            return []

        scores = []
        for doc in self.documents:
            score = 0.0
            doc_token_counts = Counter(doc["tokens"])
            doc_len = doc["doc_len"]

            for q_tok in query_tokens:
                n_q = self.doc_freqs.get(q_tok, 0)
                if n_q == 0:
                    continue

                # IDF
                idf = math.log((self.total_docs - n_q + 0.5) / (n_q + 0.5) + 1.0)
                
                # TF ve normalizasyon
                f_q = doc_token_counts.get(q_tok, 0)
                denom = f_q + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                tf_norm = (f_q * (self.k1 + 1.0)) / denom if denom > 0 else 0

                # Başlık eşleşmesi bonusu
                title_bonus = 1.5 if q_tok in normalize_turkish_token(doc["title"]) else 1.0

                score += idf * tf_norm * title_bonus

            if score > 0.0:
                snippet = self._generate_snippet(doc["raw_text"], query_tokens)
                scores.append({
                    "score": round(score, 3),
                    "title": doc["title"],
                    "rel_path": doc["rel_path"],
                    "snippet": snippet,
                    "wikilink": f"[[{doc['title']}]]"
                })

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    def _generate_snippet(self, raw_text, query_tokens, max_len=160):
        """Sorgu kelimelerinin geçtiği en iyi paragraftan kısa bir özet oluşturur."""
        lines = [l.strip() for l in raw_text.splitlines() if l.strip() and not l.startswith("---")]
        for line in lines:
            normalized_line = normalize_turkish_token(line)
            if any(q in normalized_line for q in query_tokens):
                if len(line) > max_len:
                    return line[:max_len] + "..."
                return line
        if lines:
            return lines[0][:max_len] + "..."
        return ""

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Akıllı BM25 & Türkçe Arama Motoru")
    parser.add_argument("query", type=str, help="Aranacak terim veya cümle")
    parser.add_argument("--limit", type=int, default=5, help="Maksimum sonuç sayısı (varsayılan: 5)")
    parser.add_argument("--json", action="store_true", help="Sonuçları JSON formatında yazdır")
    args = parser.parse_args()

    root = resolve_root()
    engine = BM25SearchEngine(root)
    results = engine.search(args.query, top_k=args.limit)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    print("\n" + "=" * 70)
    print(f"  SYNAPSE-AG BM25 AKILLI ARAMA SONUÇLARI: '{args.query}'")
    print(f"  İndekslenen Belge: {engine.total_docs} | Ortalama Belge Uzunluğu: {int(engine.avg_doc_len)}")
    print("=" * 70)

    if not results:
        print("[-] Hiçbir eşleşme bulunamadı.\n")
        return

    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['wikilink']} (Skor: {r['score']})")
        print(f"   Dosya: {r['rel_path']}")
        print(f"   Özet : {r['snippet']}")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
