#!/usr/bin/env python3
"""BM25 ve Türkçe Morfolojik Kök Normalizasyonu Birim Testleri."""
import sys
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from search_bm25 import normalize_turkish_token, BM25SearchEngine

class TestBM25Turkish:
    def test_consonant_softening_normalization(self):
        # b -> p
        assert normalize_turkish_token("kitabı") == "kitap"
        assert normalize_turkish_token("kitap") == "kitap"
        # ğ -> k
        assert normalize_turkish_token("örneği") == "örnek"
        assert normalize_turkish_token("örnek") == "örnek"
        # c -> ç
        assert normalize_turkish_token("ağacı") == "ağaç"
        assert normalize_turkish_token("ağaç") == "ağaç"
        # d -> t
        assert normalize_turkish_token("kanadı") == "kanat"
        assert normalize_turkish_token("kanat") == "kanat"

    def test_suffix_stemming(self):
        assert normalize_turkish_token("derslerinde") == "ders"
        assert normalize_turkish_token("notlar") == "not"
        assert normalize_turkish_token("bilgiden") == "bilgi"

    def test_bm25_search_ranking(self, tmp_path):
        # 3 adet test belgesi oluştur
        doc1 = tmp_path / "python_mimari.md"
        doc1.write_text("# Python Mimari\nBu belgede Python mimarisi ve agentic tasarım detayları anlatılmaktadır.", encoding="utf-8")

        doc2 = tmp_path / "yemek_tarifi.md"
        doc2.write_text("# Yemek Tarifi\nBugün harika bir domates çorbası pişireceğiz.", encoding="utf-8")

        engine = BM25SearchEngine(tmp_path)
        results = engine.search("python mimarisi")
        assert len(results) >= 1
        assert results[0]["title"] == "python_mimari"
