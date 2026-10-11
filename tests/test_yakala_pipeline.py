#!/usr/bin/env python3
"""Yakala Motoru ve Boru Hattı Birim Testleri."""
import sys
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from yakala import (
    capture_source,
    fetch_youtube_content,
    process_captured_cards,
    slugify,
    clipper_template,
    generate_web_clipper_template,
    get_yakala_status
)

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

    def test_web_clipper_template(self, tmp_path):
        tmpl = clipper_template("000-Inbox/Yakala")
        assert tmpl["schemaVersion"] == "0.1.0"
        assert tmpl["name"] == "Beyne at"
        assert tmpl["path"] == "000-Inbox/Yakala"
        assert any(prop["name"] == "tur" and prop["value"] == "yakala" for prop in tmpl["properties"])
        assert any(prop["name"] == "durum" and prop["value"] == "bekliyor" for prop in tmpl["properties"])

        # Dosyaya yazım testi
        out_file = generate_web_clipper_template(root=tmp_path)
        assert out_file.exists()
        assert out_file.name == "beyne-at-web-clipper.json"

    def test_process_web_clipper_card(self, tmp_path):
        inbox = tmp_path / "000-Inbox" / "Yakala"
        inbox.mkdir(parents=True, exist_ok=True)
        clipper_note = inbox / "2026-10-11-web-makale.md"
        clipper_note.write_text(
            "---\ntur: yakala\ndurum: bekliyor\nbaslik: Test Makale\n---\n\n# Test Makale\n\n## Icerik\nÖnemli araştırma metni",
            encoding="utf-8"
        )

        processed = process_captured_cards(root=tmp_path)
        assert len(processed) == 1
        content = clipper_note.read_text(encoding="utf-8")
        assert "durum: islendi" in content
        # .ham yedeği oluşturulmuş olmalı
        ham_file = inbox / ".ham" / "2026-10-11-web-makale.ham.txt"
        assert ham_file.exists()

    def test_yakala_status(self, tmp_path):
        stat = get_yakala_status(root=tmp_path)
        assert "pending" in stat
        assert "processed" in stat
        assert "tools" in stat
        assert "inbox_path" in stat

    def test_process_clippings_folder(self, tmp_path):
        clippings = tmp_path / "Clippings"
        clippings.mkdir(parents=True, exist_ok=True)
        clip_file = clippings / "MertAliiSynapse-AG.md"
        clip_file.write_text(
            "---\ntitle: 'MertAlii/Synapse-AG'\ntags:\n  - clippings\n---\n# Content",
            encoding="utf-8"
        )

        stat_before = get_yakala_status(root=tmp_path)
        assert stat_before["pending"] >= 1

        processed = process_captured_cards(root=tmp_path)
        assert len(processed) >= 1
        assert not clip_file.exists()  # taşındı

        inbox_dest = tmp_path / "000-Inbox" / "Yakala" / "MertAliiSynapse-AG.md"
        assert inbox_dest.exists()
        assert "durum: islendi" in inbox_dest.read_text(encoding="utf-8")


