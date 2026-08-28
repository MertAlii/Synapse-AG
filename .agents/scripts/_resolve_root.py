#!/usr/bin/env python3
"""Synapse-AG merkezi kök dizin çözücü. Tüm scriptler bunu import eder."""
import os
import sys
from pathlib import Path

def resolve_root():
    """Synapse-AG kök dizinini çözer.
    Öncelik sırası:
    1. SYNAPSE_AG_ROOT ortam değişkeni
    2. hooks.json payload içindeki workspacePaths (Antigravity hook'ları)
    3. Mevcut dizinde veya üst dizinlerde .beyin-version dosyası varsa orası
    4. Varsayılan: ~/.gemini/antigravity/scratch/synapse-ag/
    """
    # 1. Ortam değişkeni
    env_root = os.environ.get("SYNAPSE_AG_ROOT")
    if env_root:
        p = Path(env_root)
        if p.exists():
            return p

    # 2. Mevcut dizinden yukarı doğru .beyin-version ara
    current = Path(os.getcwd())
    for parent in [current] + list(current.parents):
        if (parent / ".beyin-version").exists():
            return parent

    # 3. Varsayılan konum
    default = Path.home() / ".gemini" / "antigravity" / "scratch" / "synapse-ag"
    if default.exists():
        return default

    # 4. Son çare: mevcut dizin
    return current


def resolve_root_from_payload(payload):
    """Antigravity hook payload'undan root çözer.
    Hook scriptleri stdin'den JSON payload alır, içinde workspacePaths olabilir.
    """
    workspace_paths = payload.get("workspacePaths", [])
    
    # workspacePaths'teki her dizini kontrol et
    for wp in workspace_paths:
        wp_path = Path(wp)
        if (wp_path / ".beyin-version").exists():
            return wp_path
    
    # workspacePaths'te bulamadıysa genel resolve'a düş
    return resolve_root()


def safe_write(file_path, content, mode="a"):
    """Dosyaya güvenli yazma. Portalocker varsa kilit alır, yoksa direkt yazar."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        import portalocker
        with portalocker.Lock(str(file_path), mode=mode, timeout=10, encoding="utf-8") as f:
            f.write(content)
    except ImportError:
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(content)


def get_version(root=None):
    """Mevcut .beyin-version değerini okur."""
    if root is None:
        root = resolve_root()
    version_file = Path(root) / ".beyin-version"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "bilinmiyor"
