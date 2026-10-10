#!/usr/bin/env python3
"""Companion Compact ve Aylık Arşivleme Birim Testleri."""
import sys
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from companion_compact import archive_companion_file, compact_file_content

class TestCompanionCompact:
    def test_archive_companion_file(self, tmp_path):
        f = tmp_path / "Last-Session.md"
        f.write_text("# Son Oturum\nDetaylar...", encoding="utf-8")

        arch_dir = tmp_path / "Arşiv" / "Companion"
        ok, msg = archive_companion_file(f, arch_dir, dry_run=False)

        assert ok is True
        archived_files = list(arch_dir.glob("Last-Session-*.md"))
        assert len(archived_files) == 1
        assert "Son Oturum" in archived_files[0].read_text(encoding="utf-8")

    def test_compact_file_content(self, tmp_path):
        f = tmp_path / "Threads.md"
        # 50 satırlık içerik
        lines = [f"Satır {i}" for i in range(50)]
        f.write_text("\n".join(lines), encoding="utf-8")

        ok, msg = compact_file_content(f, max_lines=20, dry_run=False)
        assert ok is True
        
        new_lines = f.read_text(encoding="utf-8").splitlines()
        assert len(new_lines) <= 25
        assert "Eski kayıtlar Arşiv klasörüne aktarıldı" in f.read_text(encoding="utf-8")
