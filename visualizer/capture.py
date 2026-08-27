#!/usr/bin/env python3
"""
Captures high-res screenshots of Antigravity 3D Knowledge Universe.
"""
import os
import sys
import time
import threading
import http.server
import socketserver
from pathlib import Path

PORT = 8522
ROOT_DIR = Path(__file__).parent.parent

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

def capture():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    assets_dir = ROOT_DIR / "docs" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try msedge or chromium
            try:
                browser = p.chromium.launch(channel="msedge", headless=True)
            except Exception:
                browser = p.chromium.launch(headless=True)

            page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
            url = f"http://127.0.0.1:{PORT}/visualizer/index.html"
            page.goto(url, wait_until="networkidle")
            time.sleep(3) # Wait for 3D force graph to settle

            # 1. Main 3D Graph Overview Screenshot
            shot1 = assets_dir / "preview-3d-graph.png"
            page.screenshot(path=str(shot1))
            print(f"[OK] Screenshot 1 saved: {shot1}")

            # 2. Toggle Heatmap and Screenshot
            try:
                page.click("#heatmap-btn")
                time.sleep(1.5)
                shot2 = assets_dir / "preview-heatmap.png"
                page.screenshot(path=str(shot2))
                print(f"[OK] Screenshot 2 (Heatmap) saved: {shot2}")
            except Exception as e:
                print("Heatmap shot error:", e)

            # 3. Focus on a node (Inspector Open)
            try:
                page.fill("#search-input", "Dashboard")
                time.sleep(1.5)
                shot3 = assets_dir / "preview-inspector.png"
                page.screenshot(path=str(shot3))
                print(f"[OK] Screenshot 3 (Inspector) saved: {shot3}")
            except Exception as e:
                print("Inspector shot error:", e)

            browser.close()
            print("[OK] All screenshots captured successfully!")
    except Exception as e:
        print("[!] Playwright capture error:", e)

if __name__ == "__main__":
    capture()
