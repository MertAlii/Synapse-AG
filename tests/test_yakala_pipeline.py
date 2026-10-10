#!/usr/bin/env python3
"""Yakala Motoru ve Boru Hattı Birim Testleri."""
import sys
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from yakala import capture_source, fetch_youtube_content, process_captured_cards, slugify

class TestYakalaPipeline:
    def test_slugify(self):
        assert slugify("Mert Ali Alkan İkinci Beyin") == "mert-ali-alkan-ikinci-beyin"
        assert slugify("Türkçe Karakterler: ÇĞİÖŞÜ") == "turkce-karakterler-cgiosu"

    def test_fetch_youtube_fallback(self):
        # Geçersiz / offline bir video ID verildiğinde hatasız fallback sağlamalı
        title, clean_text = fetch_youtube_content("https://www.youtube.com/watch?v=invalid_id_00")
        assert "YouTube Video" in title or "invalid_id_00" in title
        assert "invalid_id_00" in clean_text

    def test_capture_text_and_process(self, tmp_path):
        card_file, ham_file, title = capture_source(
            source_input="Ar-Ge ve yapay zeka notları",
            note="Test amacıyla yakalandı",
            root=tmp_path
        )

        assert card_file.exists()
        assert ham_file.exists()
        assert "islenmeyi_bekliyor" in card_file.read_text(encoding="utf-8")
        assert "Ar-Ge ve yapay zeka notları" in ham_file.read_text(encoding="utf-8")

        # İşleme adımı
        processed = process_captured_cards(root=tmp_path)
        assert len(processed) == 1
        assert "status: islendi" in card_file.read_text(encoding="utf-8")
