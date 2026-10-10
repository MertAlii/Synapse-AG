#!/usr/bin/env python3
"""Context Shield ve Bütçe Kalkanı Birim Testleri."""
import sys
import pytest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from inject_context import (
    is_retired_or_superseded,
    prune_rule_explanations,
    truncate_to_budget,
    MAX_CONTEXT_CHARS
)

class TestContextShield:
    def test_is_retired_or_superseded_status(self):
        content = "---\ntitle: Eski Not\nstatus: superseded\n---\nMetin"
        assert is_retired_or_superseded(content) is True

    def test_is_retired_or_superseded_turkish(self):
        content = "---\ntitle: Eski Not\nstatus: emekli\n---\nMetin"
        assert is_retired_or_superseded(content) is True

    def test_is_retired_or_superseded_tags(self):
        content = "---\ntitle: Not\ntags: [python, arşiv]\n---\nMetin"
        assert is_retired_or_superseded(content) is True

    def test_active_note_not_superseded(self):
        content = "---\ntitle: Aktif\nstatus: aktif\ntags: [core]\n---\nMetin"
        assert is_retired_or_superseded(content) is False

    def test_prune_rule_explanations(self):
        rules = (
            "- Kural: Doğrudan başla. **Neden:** Vakit kaybetme.\n"
            "- Kural: Mock kullanma. **Gerekçe:** Gerçek veri şart.\n"
            "- Kural: Testleri çalıştır. (neden: regülasyon)\n"
        )
        pruned = prune_rule_explanations(rules)
        assert "**Neden:**" not in pruned
        assert "**Gerekçe:**" not in pruned
        assert "(neden: regülasyon)" not in pruned
        assert "Doğrudan başla." in pruned
        assert "Mock kullanma." in pruned

    def test_truncate_to_budget(self):
        # 12.000 karakterlik veri üret
        long_section = "A" * 6000
        sections = [long_section, long_section]
        truncated = truncate_to_budget(sections, max_chars=MAX_CONTEXT_CHARS)
        total = sum(len(s) for s in truncated)
        assert total <= MAX_CONTEXT_CHARS
