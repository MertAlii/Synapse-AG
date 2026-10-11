#!/usr/bin/env python3
"""Çift Katmanlı Bilişsel Hafıza Birim Testleri."""
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from cognitive_memory import (
    calculate_ebbinghaus_retention,
    classify_layer,
    reinforce_memory,
    get_cognitive_report
)

class TestCognitiveMemory:
    def test_ebbinghaus_decay(self):
        # 0 gün geçtiğinde retansiyon 1.0 olmalı
        assert calculate_ebbinghaus_retention(0, 7) == 1.0
        # 7 gün geçtiğinde (t = S), R = e^(-1) ~= 0.368
        r_7 = calculate_ebbinghaus_retention(7, 7)
        assert 0.36 < r_7 < 0.38
        # Zaman arttıkça retansiyon düşmeli
        r_14 = calculate_ebbinghaus_retention(14, 7)
        assert r_14 < r_7

    def test_classify_layer(self):
        assert classify_layer("daily/2026-10-11.md") == "hippocampus"
        assert classify_layer("000-Inbox/Dump/not.md") == "hippocampus"
        assert classify_layer("500-Knowledge/Lessons.md") == "neocortex"
        assert classify_layer("knowledge/concepts/rag.md") == "neocortex"
        assert classify_layer("850-Companion/Kurallar.md") == "neocortex"

    def test_reinforce_memory(self, tmp_path):
        note_p = "daily/2026-10-11.md"
        res = reinforce_memory(note_p, root=tmp_path)
        assert res["reinforcements"] == 1
        assert res["retention_score"] == 1.0

        # İkinci pekiştirme
        res2 = reinforce_memory(note_p, root=tmp_path)
        assert res2["reinforcements"] == 2
        assert res2["stability_days"] > res["stability_days"]

    def test_cognitive_report(self, tmp_path):
        daily = tmp_path / "daily"
        daily.mkdir(parents=True, exist_ok=True)
        (daily / "2026-10-11.md").write_text("# Test Günlük Not", encoding="utf-8")

        neo = tmp_path / "500-Knowledge"
        neo.mkdir(parents=True, exist_ok=True)
        (neo / "Lessons.md").write_text("# Test Kalıcı Bilgi", encoding="utf-8")

        rep = get_cognitive_report(root=tmp_path)
        assert rep["hippocampus_count"] >= 1
        assert rep["neocortex_count"] >= 1
        assert rep["total_count"] >= 2
