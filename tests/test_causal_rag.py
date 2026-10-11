#!/usr/bin/env python3
"""Nedensellik Zinciri & Karar Ağacı RAG Birim Testleri."""
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from causal_rag import parse_lesson_blocks, parse_decision_blocks, search_causal_trajectories

class TestCausalRAG:
    def test_parse_lesson_blocks(self):
        sample = """
### [DERS-999] Test Hatası ve Kök Neden
- **Karşılaşılan Sorun / Kriz:** Model bellek sızıntısı yaptı.
- **Kök Neden:** Cache temizlenmedi ve döngüde referans tutuldu.
- **Alınan Aksiyon:** WeakRef kullanıldı, bellek serbest bırakıldı.
- **🔮 Kurallar.md'ye Eklenen Kural:** "Döngülerde referans temizliğini kontrol et."
- **Etiketler:** #leak #cache #test
"""
        trajectories = parse_lesson_blocks(sample, "test_lessons.md")
        assert len(trajectories) == 1
        item = trajectories[0]
        assert item["id"] == "DERS-999"
        assert "bellek sızıntısı" in item["problem"]
        assert "WeakRef" in item["working_solution"]
        assert "leak" in item["tags"]

    def test_parse_decision_blocks(self):
        sample = """# Mimari Karar: PostgreSQL Seçimi

## 🎯 Bağlam ve Sorun
Yüksek eşzamanlı yazma ihtiyacı.

## ⚖️ Değerlendirilen Seçenekler
SQLite denendi ancak kilitlenme yaşandı.

## ✅ Alınan Karar
PostgreSQL ve pgvector ile devam edilecek.
"""
        trajectories = parse_decision_blocks(sample, "decisions/db.md")
        assert len(trajectories) == 1
        item = trajectories[0]
        assert "PostgreSQL" in item["working_solution"]
        assert "SQLite" in item["failed_attempts"]

    def test_search_causal_trajectories(self, tmp_path):
        lessons_dir = tmp_path / "500-Knowledge"
        lessons_dir.mkdir(parents=True, exist_ok=True)
        (lessons_dir / "Lessons.md").write_text("""
### [DERS-101] React Hydration Hatası
- **Karşılaşılan Sorun / Kriz:** SSR render sırasında Text content does not match hatası.
- **Kök Neden:** Date.now() istemci ve sunucuda farklı çalıştı.
- **Alınan Aksiyon:** useEffect içinde istemci render'ına taşındı.
- **🔮 Kurallar.md'ye Eklenen Kural:** "Zaman damgalarını SSR'da doğrudan render etme."
- **Etiketler:** #react #ssr #hydration
""", encoding="utf-8")

        results = search_causal_trajectories("React hydration hatası", root=tmp_path)
        assert len(results) >= 1
        assert results[0]["id"] == "DERS-101"
        assert "useEffect" in results[0]["working_solution"]
