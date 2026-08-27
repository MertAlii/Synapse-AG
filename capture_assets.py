#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capture high-DPI screenshots of Synapse-AG features for README documentation.
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    root = Path(__file__).resolve().parent
    html_path = (root / "visualizer" / "index.html").as_uri()
    assets_dir = root / "assets" / "images"
    assets_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Visualizer URL: {html_path}")
    print(f"[*] Assets Dir: {assets_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            device_scale_factor=2
        )
        page = context.new_page()
        
        # 1. Capture 3D Knowledge Universe
        print("[1/4] Loading 3D Universe...")
        page.goto(html_path)
        page.wait_for_timeout(3500) # Wait for 3D force simulation to stabilize
        
        img1 = assets_dir / "3d-graph-universe.png"
        page.screenshot(path=str(img1))
        print(f"  -> Saved: {img1.name}")

        # 2. Capture In-App Document Reader Modal (ThreatIntel-AI or VisionRAG)
        print("[2/4] Capturing In-App Reader Modal...")
        page.evaluate("""() => {
          const node = rawData.nodes.find(n => n.id.includes('ThreatIntel') || n.id.includes('VisionRAG')) || rawData.nodes[0];
          openReader(node);
        }""")
        page.wait_for_timeout(1000)
        img2 = assets_dir / "reader-modal-view.png"
        page.screenshot(path=str(img2))
        print(f"  -> Saved: {img2.name}")

        # Close reader modal
        page.evaluate("() => closeReader()")
        page.wait_for_timeout(500)

        # 3. Capture Obsidian Vault Note Workspace
        print("[3/4] Capturing Obsidian Vault Workspace...")
        page.evaluate("""() => {
          toggleViewMode();
          const node = rawData.nodes.find(n => n.id.includes('ThreatIntel')) || rawData.nodes[0];
          renderVaultDocument(node);
        }""")
        page.wait_for_timeout(1000)
        img3 = assets_dir / "vault-note-explorer.png"
        page.screenshot(path=str(img3))
        print(f"  -> Saved: {img3.name}")

        # 4. Capture Full-Text Search with Live Snippet & Highlights
        print("[4/4] Capturing Full-Text Search in Vault...")
        page.evaluate("""() => {
          const searchInput = document.getElementById('vault-search');
          searchInput.value = 'RAG';
          filterVaultFiles('RAG');
          const node = rawData.nodes.find(n => n.id.includes('VisionRAG') || n.id.includes('RAGArchitectures')) || rawData.nodes[0];
          renderVaultDocument(node, 'RAG');
        }""")
        page.wait_for_timeout(1000)
        img4 = assets_dir / "fulltext-search-highlight.png"
        page.screenshot(path=str(img4))
        print(f"  -> Saved: {img4.name}")

        browser.close()
        print("\n[OK] All 4 documentation screenshots captured successfully!")

if __name__ == "__main__":
    main()
