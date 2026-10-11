# 📥 Synapse-AG Akıllı Yakalama Motoru (Yakala)

> **"Gördüğün yerde tek tuşla yakala; ajanın işlesin, dersleri ve çıkarımları kalıcı bilgi ağına bağlasın."**

---

## 💡 Genel Bakış

**Yakala Motoru**, internette gezinirken, araştırma yaparken veya bilgisayar başında çalışırken rastladığınız değerli kaynakları (YouTube videoları, X gönderileri, makaleler, yerel dosyalar veya anlık fikirler) kesintisiz bir şekilde **Synapse-AG** ikinci beyninize aktarmanızı sağlar.

* **🛡️ Sıfır Kirlilik (`.ham/` İzolasyonu):** Ham veriler ve uzun transkriptler `000-Inbox/Yakala/.ham/` altında izole edilir; Obsidian arama sonuçlarını ve not grafiğinizi kirletmez.
* **🔒 Yerel ve Gizlilik Odaklı:** Yakalama anında hiçbir özel veri dışarıya sızmaz (`visibility: private`).
* **🌐 Obsidian Web Clipper Tam Uyumu:** Tarayıcıdan giriş gerektiren sayfaları (Gmail, Substack, Medium, X) doğrudan içeri aktarır.
* **💻 Çapraz Platform (Windows, macOS, Linux):** Tüm işletim sistemlerinde yerel kısayol, pano ve sağ tık entegrasyonu sunar.
* **🤖 Otonom İşleme Hattı:** Antigravity içinde `"yakalananları işle"` dediğinizde bekleyen kartlar taranır, temel dersler `500-Knowledge/` veya `knowledge/concepts/` içine bağlanır.

---

## 🌐 1. Tarayıcı Entegrasyonu: Obsidian Web Clipper

[Obsidian Web Clipper](https://obsidian.md/clipper), tarayıcınızın içinden (Chrome, Firefox, Safari, Edge, Arc, Brave) herhangi bir web sayfasını, hatta oturum açılmış veya ücretli makaleleri dahi doğrudan Markdown formatında yakalamanızı sağlar.

### Kurulum (2 Dakika)

1. **Eklentiyi Kurun:** [obsidian.md/clipper](https://obsidian.md/clipper) adresinden tarayıcınıza uygun sürümü yükleyin.
2. **Şablonu Oluşturun:** Terminalinizde veya Antigravity konsolunda şu komutu çalıştırın:
   ```bash
   python .agents/scripts/yakala.py sablon
   ```
   Bu komut `000-Inbox/Yakala/beyne-at-web-clipper.json` dosyasını otomatik olarak üretir.
3. **Şablonu İçe Aktarın:**
   - Tarayıcınızda Obsidian Web Clipper simgesine tıklayın -> **Ayarlar (Settings)** açın.
   - **Şablonlar (Templates)** sekmesine gidin.
   - **İçe Aktar (Import)** butonuna tıklayıp kasanızdaki `000-Inbox/Yakala/beyne-at-web-clipper.json` dosyasını seçin.
4. **Kullanım:**
   - İstediğiniz sayfadayken Web Clipper eklenti simgesine basın.
   - Şablon olarak **"Beyne at"** seçin.
   - İsteğinize bağlı olarak **Neden** alanına kısa bir not yazın ve **Add (Ekle)** butonuna basın.
   - Sayfa anında kasanızın `000-Inbox/Yakala/` klasörüne temiz bir kart olarak düşer.

---

## 🖥️ 2. İşletim Sistemi ve Masaüstü Entegrasyonu

Synapse-AG, Windows, macOS ve Linux üzerinde yerel araçlarla tam uyumlu çalışır.

### Windows (Sağ Tık "Gönder > Beyne At" & Kısayol)

Kurulum betiğini tek seferlik çalıştırın:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\kur_yakala_windows.ps1
```
* **Dosya Yakalama:** Masaüstünde veya Dosya Gezgini'nde herhangi bir dosyaya (PDF, TXT, kod) sağ tıklayın -> **Gönder (Send to)** -> **Beyne At** seçin.
* **Pano Yakalama:** Panodaki metin veya bağlantıyı yakalamak için:
  ```powershell
  py -3 .agents\scripts\yakala.py --clipboard
  ```

---

### macOS (Kısayollar & CLI)

Kurulum betiğini çalıştırın:
```bash
bash scripts/kur_yakala_macos.sh
```
* Bu betik `~/.local/bin/beyne-at` sarmalayıcısını oluşturur ve Web Clipper şablonunu hazırlar.
* **Sistem Kısayolu Atama (Control+Option+B):**
  1. macOS **Kısayollar (Shortcuts)** uygulamasını açın -> Yeni Kısayol oluşturun.
  2. Eylem olarak **"Kabuk Betiği Çalıştır" (Run Shell Script)** ekleyin.
  3. Komut kutusuna `~/.local/bin/beyne-at` yazın.
  4. Sağ kenar çubuğundan Kısayol Tuşu olarak `Control+Option+B` belirleyin.
* **Pano:** `pbpaste` desteği ile panodaki metinleri otomatik çeker.

---

### Linux (GNOME, KDE Plasma, Hyprland, X11/Wayland)

Kurulum betiğini çalıştırın:
```bash
bash scripts/kur_yakala_linux.sh
```
* Bu betik `~/.local/bin/beyne-at` komutunu ve `~/.local/share/applications/beyne-at.desktop` masaüstü girdisini oluşturur.
* **Pano Desteği:** Wayland ortamında `wl-paste` (`wl-clipboard`), X11 ortamında `xclip` veya `xsel` kullanılır.
* **Klavye Kısayolu Atama (Ctrl+Alt+B):**
  - **GNOME:** Ayarlar > Klavye > Özel Kısayollar > Ekle (`+`) -> Komut: `~/.local/bin/beyne-at` -> Tuş: `Ctrl+Alt+B`.
  - **KDE Plasma:** Sistem Ayarları > Kısayollar > Özel Kısayol Ekle -> Komut: `~/.local/bin/beyne-at`.
  - **Hyprland / Sway:** `bind = $mainMod ALT, B, exec, ~/.local/bin/beyne-at`

---

## 🎬 3. Komut Satırı ve YouTube Yakalama

### Doğrudan Kaynak Yakalama

```bash
# YouTube Videosu (Transkript, kanal ve meta verileri otomatik çıkarılır)
python .agents/scripts/yakala.py "https://www.youtube.com/watch?v=..." --note "Yeni mimari incelemesi"

# Web Makalesi veya Dokümantasyon
python .agents/scripts/yakala.py "https://arxiv.org/abs/..." --note "Agentic reasoning makalesi"

# Yerel Dosya
python .agents/scripts/yakala.py "proje-taslagi.pdf" --note "İnceleme için"

# Panodaki Metin (Clipboard)
python .agents/scripts/yakala.py --clipboard --note "Hızlı not"
```

### Durum ve Kuyruk Raporu

```bash
python .agents/scripts/yakala.py durum
```
Çıktı örneği:
```text
=======================================================
             SYNAPSE-AG YAKALA DURUM RAPORU
=======================================================
Klasör        : 000-Inbox/Yakala
Bekleyen Kart : 3
İşlenen Kart  : 14
Toplam Kart   : 17
-------------------------------------------------------
Araç Durumu:
  * youtube_transcript_api   : [OK] Yüklü
  * yt-dlp                   : [OK] Yüklü
  * web_clipper_sablonu      : [OK] Yüklü
=======================================================
```

---

## 🔄 4. Yakalananları İşleme ("yakalananları işle")

Yakaladığınız ham içerikleri kalıcı bilgiye dönüştürmek için:

**Antigravity Sohbetinde:**
> *"Yakalananları işle"* veya *"Gelen kutusundaki yeni kaynakları sentezle"*

**Komut Satırında:**
```bash
python .agents/scripts/yakala.py process
```

Bu işlem:
1. `status: islenmeyi_bekliyor` veya Web Clipper'dan gelen `durum: bekliyor` kartlarını tespit eder.
2. Anahtar içgörüleri ve dersleri özetler.
3. Ham dökümü `.ham/` klasörüne arşivler.
4. `500-Knowledge/` veya `knowledge/concepts/` içinde ilgili kavramlara bağlantı (`[[Wikilink]]`) kurar.
5. Kartı `status: islendi` / `durum: islendi` olarak günceller.

---

## 📂 Dosya Hiyerarşisi

```text
Synapse-AG/
└── 000-Inbox/ (veya 📥 000-Inbox/)
    └── Yakala/
        ├── beyne-at-web-clipper.json                    # Obsidian Web Clipper şablonu
        ├── .ham/                                        # Gizli ham dökümler (aramada görünmez)
        │   └── 20261011_kaynak.ham.txt
        └── 20261011_kaynak.md                           # Obsidian Yakalama Kartı (Frontmatter + Özet)
```
