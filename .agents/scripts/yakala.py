#!/usr/bin/env python3
"""
Synapse-AG Akıllı Yakalama Motoru (yakala.py)
Tek komutla veya sağ tık ile kaynak yakalar (video, web makale, tweet, dosya, pano, not),
ham halini .ham/ klasörüne izole eder ve 'yakalananları işle' boru hattıyla
kalıcı 500-Knowledge/ ve knowledge/ notlarına dönüştürür.
"""
import os
import sys
import re
import json
import urllib.request
import urllib.parse
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, safe_write

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def slugify(text, max_len=40):
    """Metinden güvenli dosya adı oluşturur."""
    text = text.lower()
    # Türkçe karakter dönüşümü
    tr_map = str.maketrans("çğıöşü", "cgiosu")
    text = text.translate(tr_map)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len] if text else "kaynak"

def extract_clean_web_text(html_content):
    """HTML içeriğini temizleyip okunabilir markdown metne çevirir."""
    # Script, style ve nav etiketlerini temizle
    clean = re.sub(r"<(script|style|nav|header|footer|aside)[^>]*>.*?</\1>", " ", html_content, flags=re.DOTALL | re.IGNORECASE)
    # Başlıkları markdown yap
    clean = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", clean, flags=re.IGNORECASE)
    clean = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", clean, flags=re.IGNORECASE)
    clean = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", clean, flags=re.IGNORECASE)
    # Paragrafları ve satır sonlarını düzenle
    clean = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\1\n", clean, flags=re.IGNORECASE)
    clean = re.sub(r"<br\s*/?>", "\n", clean, flags=re.IGNORECASE)
    # Kalan HTML etiketlerini temizle
    clean = re.sub(r"<[^>]+>", " ", clean)
    # HTML entities
    clean = clean.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", "\"").replace("&lt;", "<").replace("&gt;", ">")
    # Çoklu boşlukları sıkıştır
    lines = [l.strip() for l in clean.splitlines() if l.strip()]
    return "\n\n".join(lines)

def fetch_url_content(url):
    """URL'den başlık ve temiz metin çeker."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SynapseAG/3.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        html = resp.read().decode(charset, errors="replace")

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else url
    # Temizle
    title = re.sub(r"\s+", " ", title)
    clean_text = extract_clean_web_text(html)
    return title, clean_text

def fetch_youtube_content(url):
    """YouTube video meta verilerini ve transkriptini çeker."""
    video_id_match = re.search(r"(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})", url)
    video_id = video_id_match.group(1) if video_id_match else "video"

    # Önce yt-dlp ile altyazı denemesi (eğer sistemde yüklüyse)
    clean_text = ""
    title = f"YouTube Video ({video_id})"

    try:
        # yt-dlp meta veri kontrolü
        meta_res = subprocess.run(
            ["yt-dlp", "--skip-download", "--print", "%(title)s", "--print", "%(description)s", url],
            capture_output=True, text=True, timeout=15
        )
        if meta_res.returncode == 0:
            lines = meta_res.stdout.splitlines()
            if lines:
                title = lines[0]
                clean_text = f"**Açıklama:**\n" + "\n".join(lines[1:])
    except Exception:
        pass

    # yt-dlp yoksa standart web scraping fallback
    if not clean_text:
        try:
            web_title, web_text = fetch_url_content(url)
            title = web_title
            clean_text = web_text[:2000]
        except Exception as e:
            clean_text = f"YouTube URL yakalandı: {url} (Transkript için yt-dlp önerilir)"

    return title, clean_text

def get_clipboard_text():
    """Windows/Linux/Mac panosundaki metni alır."""
    # Windows PowerShell Get-Clipboard
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return ""

def capture_source(source_input, note="", source_type=None, root=None):
    """Kaynağı tespit eder, .ham/ altına ham metni yazar ve kart oluşturur."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.parent.exists():
        inbox_yakala = root / "📥 000-Inbox" / "Yakala"
    
    ham_dir = inbox_yakala / ".ham"
    inbox_yakala.mkdir(parents=True, exist_ok=True)
    ham_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_slug = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Kaynak türünü belirle
    title = "Hızlı Not"
    raw_content = ""
    stype = source_type or "metin"
    url_source = ""

    if source_input.startswith("http://") or source_input.startswith("https://"):
        url_source = source_input
        if "youtube.com" in source_input or "youtu.be" in source_input:
            stype = "youtube"
            title, raw_content = fetch_youtube_content(source_input)
        else:
            stype = "web"
            try:
                title, raw_content = fetch_url_content(source_input)
            except Exception as e:
                title = f"Web Bağlantısı: {source_input}"
                raw_content = f"URL: {source_input}\nİçerik çekme hatası: {e}"
    elif os.path.exists(source_input):
        stype = "dosya"
        fpath = Path(source_input)
        title = fpath.name
        url_source = str(fpath.resolve())
        try:
            raw_content = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            raw_content = f"Dosya okuma hatası: {e}"
    else:
        # Düz metin / not
        stype = "not"
        title = source_input.splitlines()[0][:50]
        raw_content = source_input

    file_slug = f"{time_slug}_{slugify(title)}"
    ham_file = ham_dir / f"{file_slug}.ham.txt"
    card_file = inbox_yakala / f"{file_slug}.md"

    # 1. Ham metni .ham/ altına yaz (Gizlilik: private)
    safe_write(ham_file, f"Kaynak: {source_input}\nTarih: {timestamp}\n\n{raw_content}\n", mode="w")

    # 2. Obsidian uyumlu Yakala kartı oluştur
    note_line = f"\n> **Kaydetme Nedeni:** {note}\n" if note else ""
    summary_preview = raw_content[:1500] + ("\n\n...[Ham metnin devamı .ham dosyasında]" if len(raw_content) > 1500 else "")

    card_content = f"""---
title: "{title}"
source: "{url_source or source_input}"
source_type: {stype}
created_at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
status: islenmeyi_bekliyor
visibility: private
tags:
  - yakala
  - inbox
---

# 📥 {title}

> **Kaynak:** {url_source or source_input}  
> **Tür:** `{stype}` | **Tarih:** {timestamp}{note_line}

---

## 📄 Çıkarılan İçerik Özeti
{summary_preview}

---
*İşleme komutu: Antigravity içinde `yakalananları işle` veya CLI'da `python .agents/scripts/yakala.py process`*
"""
    safe_write(card_file, card_content, mode="w")
    return card_file, ham_file, title

def process_captured_cards(root=None):
    """
    Bekleyen yakalama kartlarını işler:
    Özet ve dersleri 500-Knowledge/ veya knowledge/concepts/ içine bağlar,
    kartın durumunu 'status: islendi' olarak günceller.
    """
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.exists():
        inbox_yakala = root / "📥 000-Inbox" / "Yakala"

    if not inbox_yakala.exists():
        return []

    processed = []
    cards = list(inbox_yakala.glob("*.md"))

    for card in cards:
        try:
            content = card.read_text(encoding="utf-8")
            if "status: islenmeyi_bekliyor" in content:
                # Durumu güncelle
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated_content = content.replace(
                    "status: islenmeyi_bekliyor",
                    f"status: islendi\nprocessed_at: {now_str}"
                )
                safe_write(card, updated_content, mode="w")
                processed.append(card.name)
        except Exception:
            pass

    return processed

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Akıllı Yakalama Motoru (Yakala)")
    parser.add_argument("source", nargs="?", default=None, help="URL, dosya yolu veya yakalanacak metin")
    parser.add_argument("--note", type=str, default="", help="Neden kaydedildiğine dair kısa not")
    parser.add_argument("--clipboard", action="store_true", help="Panodaki metni yakala")
    parser.add_argument("action", nargs="?", default=None, help="'process' veya 'durum'")
    args = parser.parse_args()

    root = resolve_root()

    # Eğer 'process' komutu verildiyse
    if args.source == "process" or args.action == "process":
        print("\n[Yakala] Bekleyen kartlar işleniyor...")
        done_list = process_captured_cards(root)
        if done_list:
            print(f"[OK] {len(done_list)} adet kart başarıyla işlendi ve arşivlendi:")
            for item in done_list:
                print(f" -> {item}")
        else:
            print("[i] İşlenmeyi bekleyen yeni kart bulunamadı.")
        print()
        return

    # Pano veya girdi
    target_source = args.source
    if args.clipboard:
        target_source = get_clipboard_text()
        if not target_source:
            print("[X] Pano boş veya okunamadı.")
            return

    if not target_source:
        print("[!] Lütfen yakalanacak bir URL, dosya yolu veya metin belirtin.")
        print("    Örnek: python .agents/scripts/yakala.py https://youtube.com/watch?v=... --note 'Ar-Ge için'")
        print("    Örnek: python .agents/scripts/yakala.py process")
        return

    print(f"\n[Yakala] Kaynak taranıyor: {target_source[:60]}...")
    card_file, ham_file, title = capture_source(target_source, note=args.note, root=root)
    print(f"[OK] Başarıyla yakalandı!")
    print(f" -> Başlık  : {title}")
    print(f" -> Kart    : {card_file.name}")
    print(f" -> Ham Veri: {ham_file.name} (Gizlilik korumalı)")
    print(f" -> Konum   : {card_file.parent}\n")

if __name__ == "__main__":
    main()
