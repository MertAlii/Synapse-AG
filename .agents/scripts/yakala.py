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

    title = f"YouTube Video ({video_id})"
    author = "Bilinmeyen Kanal"
    author_url = ""
    transcript_text = ""

    # 1. YouTube oEmbed API ile resmi ve temiz meta veri alımı
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0 SynapseAG/3.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            title = data.get("title", title)
            author = data.get("author_name", "Bilinmeyen Kanal")
            author_url = data.get("author_url", "")
    except Exception:
        pass

    # 2. youtube_transcript_api ile doğrudan altyazı / transkript çekimi
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcripts = api.list(video_id)
        target_t = None
        # Önce Türkçe transkript ara
        for t in transcripts:
            if t.language_code.startswith("tr"):
                target_t = t
                break
        # Bulunamazsa mevcut herhangi bir transkripti al
        if not target_t:
            for t in transcripts:
                target_t = t
                break
        
        if target_t:
            items = target_t.fetch()
            transcript_text = " ".join([item.text for item in items if item.text])
    except Exception:
        pass

    # 3. Transkript yoksa yt-dlp dene (eğer sistemde yüklüyse)
    if not transcript_text:
        try:
            meta_res = subprocess.run(
                ["yt-dlp", "--skip-download", "--print", "%(title)s", "--print", "%(description)s", url],
                capture_output=True, text=True, timeout=15
            )
            if meta_res.returncode == 0:
                lines = meta_res.stdout.splitlines()
                if lines:
                    title = lines[0]
                    transcript_text = "\n".join(lines[1:])
        except Exception:
            pass

    # 4. Fallback web scraping
    if not transcript_text:
        try:
            web_title, web_text = fetch_url_content(url)
            if web_title and web_title.strip() not in ["- YouTube", "YouTube"]:
                title = web_title
            transcript_text = web_text[:2000]
        except Exception:
            pass

    # Metni biçimlendir
    header_block = (
        f"- **Kanal:** [{author}]({author_url})\n"
        f"- **Video ID:** `{video_id}`\n"
        f"- **Video URL:** {url}\n\n"
        f"![Kapak Resmi](https://i.ytimg.com/vi/{video_id}/hqdefault.jpg)\n\n"
    )

    if transcript_text:
        word_count = len(transcript_text.split())
        clean_text = header_block + f"### 🎙️ Video Transkripti & Konuşma Metni ({word_count:,} Kelime)\n\n{transcript_text}"
    else:
        clean_text = header_block + "\n*(Bu video için altyazı veya konuşma metni bulunamadı.)*"

    return title, clean_text

def get_clipboard_text():
    """Windows/Linux/macOS panosundaki metni alır."""
    platform = sys.platform

    # 1. macOS (pbpaste)
    if platform == "darwin":
        try:
            res = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass

    # 2. Linux (Wayland: wl-paste, X11: xclip / xsel)
    elif platform.startswith("linux"):
        if os.environ.get("WAYLAND_DISPLAY"):
            try:
                res = subprocess.run(["wl-paste"], capture_output=True, text=True, timeout=5)
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip()
            except Exception:
                pass
        try:
            res = subprocess.run(["xclip", "-selection", "clipboard", "-o"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
        try:
            res = subprocess.run(["xsel", "-b", "-o"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass

    # 3. Windows (PowerShell Get-Clipboard)
    elif platform == "win32":
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass

    # Fallback: Tkinter (Tüm işletim sistemleri)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        text = root.clipboard_get()
        root.destroy()
        if text and text.strip():
            return text.strip()
    except Exception:
        pass

    return ""

def clipper_template(inbox_path=None):
    """
    Obsidian Web Clipper (https://obsidian.md/clipper) import şablonu üretir.
    Kullanıcı bu JSON dosyasını Clipper ayarlarına aktardığında tek tıkla web sayfalarını,
    giriş gerektiren içerikleri ve seçimleri doğrudan kasaya kaydeder.
    """
    target_path = inbox_path or "000-Inbox/Yakala"
    return {
        "schemaVersion": "0.1.0",
        "name": "Beyne at",
        "behavior": "create",
        "noteNameFormat": '{{date|date:"YYYY-MM-DD-HHmm"}}-{{title|safe_name|lower|slice:0,48}}',
        "path": target_path,
        "noteContentFormat": "# {{title}}\n\n## Neden\n\n\n\n## Kaynak\n\n{{url}}\n\n## Secim\n\n{{selection}}\n\n## Icerik\n\n{{content}}\n",
        "properties": [
            {"name": "tur", "value": "yakala", "type": "text"},
            {"name": "durum", "value": "bekliyor", "type": "text"},
            {"name": "kaynak_turu", "value": "", "type": "text"},
            {"name": "baslik", "value": "{{title}}", "type": "text"},
            {"name": "url", "value": "{{url}}", "type": "text"},
            {"name": "yakalandi", "value": '{{date|date:"YYYY-MM-DDTHH:mm:ssZ"}}', "type": "text"},
            {"name": "arac", "value": "web-clipper", "type": "text"},
            {"name": "visibility", "value": "internal", "type": "text"}
        ],
        "triggers": []
    }

def generate_web_clipper_template(root=None):
    """Web clipper JSON şablonunu inbox klasörüne yazar ve dosya yolunu döner."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.parent.exists() and (root / "📥 000-Inbox").exists():
        inbox_yakala = root / "📥 000-Inbox" / "Yakala"

    inbox_yakala.mkdir(parents=True, exist_ok=True)
    (inbox_yakala / ".ham").mkdir(parents=True, exist_ok=True)

    try:
        rel_inbox = str(inbox_yakala.relative_to(root)).replace("\\", "/")
    except Exception:
        rel_inbox = "000-Inbox/Yakala"

    data = clipper_template(rel_inbox)
    target_file = inbox_yakala / "beyne-at-web-clipper.json"
    safe_write(target_file, json.dumps(data, ensure_ascii=False, indent=2) + "\n", mode="w")
    return target_file

def capture_source(source_input, note="", source_type=None, root=None):
    """Kaynağı tespit eder, .ham/ altına ham metni yazar ve kart oluşturur."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.parent.exists() and (root / "📥 000-Inbox").exists():
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
    - 'status: islenmeyi_bekliyor' (CLI/otomatik) veya
    - 'durum: bekliyor' (Obsidian Web Clipper) kartlarını tespit eder.
    Özet ve dersleri bağlar, ham metni .ham/ altına taşır (yoksa),
    kart durumunu 'status: islendi' / 'durum: islendi' olarak günceller.
    """
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.exists() and (root / "📥 000-Inbox" / "Yakala").exists():
        inbox_yakala = root / "📥 000-Inbox" / "Yakala"

    if not inbox_yakala.exists():
        return []

    ham_dir = inbox_yakala / ".ham"
    ham_dir.mkdir(parents=True, exist_ok=True)

    processed = []
    cards = sorted(list(inbox_yakala.glob("*.md")))

    for card in cards:
        try:
            content = card.read_text(encoding="utf-8")
            is_pending = False
            updated = content

            if "status: islenmeyi_bekliyor" in content:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = updated.replace(
                    "status: islenmeyi_bekliyor",
                    f"status: islendi\nprocessed_at: {now_str}"
                )
                is_pending = True

            if "durum: bekliyor" in content:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = updated.replace(
                    "durum: bekliyor",
                    f"durum: islendi\nislenme_tarihi: {now_str}"
                )
                is_pending = True

            if is_pending:
                # Web Clipper ile gelmişse ve .ham dosyası yoksa ham yedeği oluştur
                ham_file = ham_dir / f"{card.stem}.ham.txt"
                if not ham_file.exists():
                    safe_write(ham_file, f"Kaynak Kart: {card.name}\n\n{content}\n", mode="w")

                safe_write(card, updated, mode="w")
                processed.append(card.name)
        except Exception:
            pass

    return processed

def get_yakala_status(root=None):
    """Yakala kuyruğunun durumunu ve sistem araçlarını raporlar."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    inbox_yakala = root / "000-Inbox" / "Yakala"
    if not inbox_yakala.exists() and (root / "📥 000-Inbox" / "Yakala").exists():
        inbox_yakala = root / "📥 000-Inbox" / "Yakala"

    pending_count = 0
    processed_count = 0
    total_count = 0

    if inbox_yakala.exists():
        cards = list(inbox_yakala.glob("*.md"))
        total_count = len(cards)
        for c in cards:
            try:
                txt = c.read_text(encoding="utf-8", errors="ignore")
                if "status: islenmeyi_bekliyor" in txt or "durum: bekliyor" in txt:
                    pending_count += 1
                elif "status: islendi" in txt or "durum: islendi" in txt:
                    processed_count += 1
            except Exception:
                pass

    tools = {}
    try:
        import youtube_transcript_api
        tools["youtube_transcript_api"] = True
    except ImportError:
        tools["youtube_transcript_api"] = False

    try:
        res = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, timeout=5)
        tools["yt-dlp"] = (res.returncode == 0)
    except Exception:
        tools["yt-dlp"] = False

    clipper_file = inbox_yakala / "beyne-at-web-clipper.json" if inbox_yakala.exists() else None
    tools["web_clipper_sablonu"] = clipper_file.exists() if clipper_file else False

    try:
        rel_path = str(inbox_yakala.relative_to(root)).replace("\\", "/")
    except Exception:
        rel_path = "000-Inbox/Yakala"

    return {
        "inbox_path": rel_path,
        "pending": pending_count,
        "processed": processed_count,
        "total": total_count,
        "tools": tools
    }

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Akıllı Yakalama Motoru (Yakala)")
    parser.add_argument("source", nargs="?", default=None, help="URL, dosya yolu, metin veya alt komut (process/durum/sablon/kur)")
    parser.add_argument("--note", type=str, default="", help="Neden kaydedildiğine dair kısa not")
    parser.add_argument("--clipboard", action="store_true", help="Panodaki metni yakala")
    parser.add_argument("--sablon", action="store_true", help="Obsidian Web Clipper şablonunu oluştur / göster")
    parser.add_argument("action", nargs="?", default=None, help="'process', 'durum', 'sablon' veya 'kur'")
    args = parser.parse_args()

    root = resolve_root()

    # Alt komut kontrolü
    cmd = args.source or args.action
    if args.sablon or cmd in ["sablon", "clipper"]:
        target_json = generate_web_clipper_template(root)
        print("\n[OK] Obsidian Web Clipper Şablonu Hazırlandı:")
        print(f" -> Dosya: {target_json}")
        print("\nKurulum Adımları:")
        print(" 1. https://obsidian.md/clipper adresinden tarayıcı eklentisini kurun.")
        print(" 2. Eklenti Ayarları > Şablonlar > İçe Aktar (Import) ile yukarıdaki JSON dosyasını seçin.")
        print(" 3. İstediğiniz web sayfasında 'Beyne at' şablonuna basıp kaydedin.\n")
        return

    if cmd in ["kur", "setup"]:
        target_json = generate_web_clipper_template(root)
        print("\n=======================================================")
        print("       SYNAPSE-AG YAKALA ENTEGRASYON KURULUMU")
        print("=======================================================")
        print(f"[OK] Web Clipper şablonu yazıldı: {target_json.name}")
        print("\nMasaüstü & Kısayol Entegrasyonu:")
        if sys.platform == "win32":
            print(" -> Windows: Sağ tık 'Gönder > Beyne At' için scripts\\kur_yakala_windows.ps1 çalıştırın.")
        elif sys.platform == "darwin":
            print(" -> macOS: scripts/kur_yakala_macos.sh çalıştırın (Control+Option+B kısayolu).")
        else:
            print(" -> Linux: scripts/kur_yakala_linux.sh çalıştırın (Ctrl+Alt+B kısayolu).")
        print("=======================================================\n")
        return

    if cmd in ["durum", "status"]:
        stat = get_yakala_status(root)
        print("\n=======================================================")
        print("             SYNAPSE-AG YAKALA DURUM RAPORU")
        print("=======================================================")
        print(f"Klasör        : {stat['inbox_path']}")
        print(f"Bekleyen Kart : {stat['pending']}")
        print(f"İşlenen Kart  : {stat['processed']}")
        print(f"Toplam Kart   : {stat['total']}")
        print("-------------------------------------------------------")
        print("Araç Durumu:")
        for tname, tok in stat["tools"].items():
            tstatus = "[OK] Yüklü" if tok else "[-] Yok"
            print(f"  * {tname:<25}: {tstatus}")
        print("=======================================================\n")
        return

    if cmd in ["process", "isle"]:
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
        print("    Örnekler:")
        print("      python .agents/scripts/yakala.py https://youtube.com/watch?v=... --note 'Ar-Ge'")
        print("      python .agents/scripts/yakala.py --clipboard")
        print("      python .agents/scripts/yakala.py sablon   (Web Clipper JSON şablonu)")
        print("      python .agents/scripts/yakala.py durum    (Kuyruk ve araç durumu)")
        print("      python .agents/scripts/yakala.py process  (Bekleyen kartları işle)")
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
