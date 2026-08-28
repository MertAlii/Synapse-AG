#!/usr/bin/env python3
"""Synapse-AG betik birim testleri."""
import sys
import os
import tempfile
import json
from pathlib import Path

# Script dizinini path'e ekle
SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from _resolve_root import resolve_root, resolve_root_from_payload, safe_write, get_version


class TestResolveRoot:
    """resolve_root fonksiyon testleri."""

    def test_env_var_override(self, tmp_path):
        """SYNAPSE_AG_ROOT ortam değişkeni öncelikli olmalı."""
        os.environ["SYNAPSE_AG_ROOT"] = str(tmp_path)
        try:
            result = resolve_root()
            assert result == tmp_path
        finally:
            del os.environ["SYNAPSE_AG_ROOT"]

    def test_beyin_version_detection(self, tmp_path):
        """Dizinde .beyin-version varsa o dizini dönmeli."""
        version_file = tmp_path / ".beyin-version"
        version_file.write_text("2.1.0")
        
        # Simüle: cwd'yi tmp_path yap
        old_cwd = os.getcwd()
        os.chdir(str(tmp_path))
        try:
            # env var temizle
            os.environ.pop("SYNAPSE_AG_ROOT", None)
            result = resolve_root()
            assert result == tmp_path
        finally:
            os.chdir(old_cwd)

    def test_payload_resolution(self, tmp_path):
        """workspacePaths içinden .beyin-version olan dizini bulmalı."""
        vault = tmp_path / "my-vault"
        vault.mkdir()
        (vault / ".beyin-version").write_text("2.1.0")
        
        payload = {"workspacePaths": [str(vault)]}
        result = resolve_root_from_payload(payload)
        assert result == vault


class TestSafeWrite:
    """safe_write fonksiyon testleri."""

    def test_write_creates_file(self, tmp_path):
        """Dosya yoksa oluşturmalı."""
        target = tmp_path / "sub" / "test.md"
        safe_write(target, "merhaba\n", mode="w")
        assert target.exists()
        assert target.read_text(encoding="utf-8") == "merhaba\n"

    def test_append_mode(self, tmp_path):
        """Append modunda mevcut içeriği korumalı."""
        target = tmp_path / "test.md"
        target.write_text("ilk satır\n", encoding="utf-8")
        safe_write(target, "ikinci satır\n", mode="a")
        content = target.read_text(encoding="utf-8")
        assert "ilk satır" in content
        assert "ikinci satır" in content


class TestGetVersion:
    """get_version fonksiyon testleri."""

    def test_reads_version(self, tmp_path):
        (tmp_path / ".beyin-version").write_text("2.1.0")
        assert get_version(tmp_path) == "2.1.0"

    def test_missing_version(self, tmp_path):
        assert get_version(tmp_path) == "bilinmiyor"
