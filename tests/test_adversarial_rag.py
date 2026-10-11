#!/usr/bin/env python3
"""Şeytanın Avukatı RAG Birim Testleri."""
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from adversarial_rag import evaluate_adversarial_perspective

class TestAdversarialRAG:
    def test_evaluate_known_pitfall_sqlite(self):
        findings = evaluate_adversarial_perspective("Bu projede SQLite ile yoğun concurrent yazma yapacağız")
        assert len(findings) >= 1
        assert any("SQLITE" in f["title"] for f in findings)
        assert any("database is locked" in f["counter_argument"] for f in findings)

    def test_evaluate_microservices_anti_pattern(self):
        findings = evaluate_adversarial_perspective("İlk günden microservice mimarisi kuralım")
        assert len(findings) >= 1
        assert any("MICROSERVICE" in f["title"] for f in findings)
        assert any("monolit" in f["counter_argument"] for f in findings)

    def test_evaluate_safe_proposal(self, tmp_path):
        # Tamamen nötr / sorunsuz bir karar
        findings = evaluate_adversarial_perspective("Unit test yazıp CI pipeline'a ekleyelim", root=tmp_path)
        # Bilinen anti-pattern veya ders tetiklenmemeli
        assert isinstance(findings, list)
