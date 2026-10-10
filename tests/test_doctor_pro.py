#!/usr/bin/env python3
"""Doctor Pro 2.0 Sağlık Denetimi Birim Testleri."""
import sys
import os
import time
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from doctor import check_git_conflict_markers, check_inbox_aging, check_supersedes_and_inferences

class TestDoctorPro:
    def test_git_conflict_markers_detection(self, tmp_path):
        clean_file = tmp_path / "clean.md"
        clean_file.write_text("# Baslik\nIcerik", encoding="utf-8")

        broken_file = tmp_path / "conflict.md"
        broken_file.write_text("# Baslik\n<<<<<<<\nlocal\n=======\nremote\n>>>>>>>\n", encoding="utf-8")

        conflicts = check_git_conflict_markers(tmp_path)
        assert len(conflicts) == 1
        assert Path(conflicts[0]).name == "conflict.md"

    def test_inbox_aging_detection(self, tmp_path):
        inbox = tmp_path / "000-Inbox"
        inbox.mkdir()

        fresh_file = inbox / "yeni.md"
        fresh_file.write_text("# Yeni Not", encoding="utf-8")

        old_file = inbox / "eski.md"
        old_file.write_text("# Eski Not", encoding="utf-8")
        
        # Dosya zamanını 10 gün öncesine ayarla
        ten_days_ago = time.time() - (10 * 86400)
        os.utime(str(old_file), (ten_days_ago, ten_days_ago))

        report = check_inbox_aging(tmp_path, max_days=7, max_items=10)
        assert report["total_items"] == 2
        assert report["old_items_count"] == 1
        assert report["is_warning"] is True

    def test_supersedes_detection(self, tmp_path):
        note = tmp_path / "retired_note.md"
        note.write_text("---\ntitle: Eski Plan\nstatus: superseded\n---\nDetay", encoding="utf-8")

        res = check_supersedes_and_inferences(tmp_path)
        assert len(res) == 1
        assert "retired_note.md" in res[0]
