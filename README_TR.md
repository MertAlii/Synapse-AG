<p align="center">
  <img src="docs/assets/synapse-logo.png" alt="Synapse-AG Logo" width="160px" style="border-radius: 28px; box-shadow: 0 12px 35px rgba(251, 113, 133, 0.35);" />
</p>

<h1 align="center">Synapse-AG</h1>

<p align="center">
  <b>Google Antigravity 2.0 & Obsidian için Kendi Kendine Hatırlayan, Otonom İkinci Beyin & Bilgi Motoru</b>
</p>

<p align="center">
  <a href="README.md">🇬🇧 <b>Click for English Documentation</b></a>
</p>

<p align="center">
  <a href="#-lisans--kaynaklar"><img src="https://img.shields.io/badge/Lisans-MIT-pink.svg?style=for-the-badge" alt="License MIT"></a>
  <a href="#-tek-komutla-hızlı-kurulum"><img src="https://img.shields.io/badge/Motor-Antigravity_2.0-blue.svg?style=for-the-badge&logo=google" alt="Antigravity 2.0"></a>
  <a href="#-obsidian-entegrasyonu"><img src="https://img.shields.io/badge/Obsidian-Hazır_Vault-purple.svg?style=for-the-badge&logo=obsidian" alt="Obsidian"></a>
  <a href="#-mimari-yapı"><img src="https://img.shields.io/badge/Depolama-%25100_Markdown-emerald.svg?style=for-the-badge" alt="Markdown"></a>
  <a href="https://github.com/MertAlii/Synapse-AG"><img src="https://img.shields.io/badge/PR'lar-Açık-brightgreen.svg?style=for-the-badge" alt="PRs Welcome"></a>
</p>

<p align="center">
  <img src="assets/images/obsidian-graph.png" alt="Synapse-AG Obsidian Bilgi Grafiği" width="100%" style="border-radius: 14px; box-shadow: 0 25px 60px rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.08);" />
</p>

---

## 💡 Genel Bakış

**Synapse-AG**, **Google Antigravity 2.0** ve **Obsidian** üzerinde çalışan, oturumlar arası hafızası **kendi kendine yazılan ve asla kaybolmayan** yerel bir "İkinci Beyin" ekosistemidir.

* **🧠 Oturumlar Arası Kalıcı Hafıza:** Yaşam döngüsü kancaları (`PreInvocation`, `Stop`) oturum açılışında önceki hafızayı otomatik bağlama aktarır, oturum bittiğinde ise konuşmayı `daily/YYYY-MM-DD.md` içine işler.
* **📚 Otonom Bilgi Derleyicisi:** Günlük ham notlar, Andrej Karpathy'nin LLM Bilgi Tabanı desenine göre `knowledge/concepts/` ve `knowledge/connections/` altında kalıcı makalelere dönüştürülür.
* **💎 Doğrudan Obsidian Entegrasyonu:** Renk kodlu kategorilere sahip Graph View (`Ctrl+G`), Günlük Notlar, Şablonlar, Canvas ve çift yönlü `[[Wikilinks]]` bağlantıları hazır gelir.
* **🛡️ Sıfır Veri Kayıplı Güncelleme:** Semantik sürüm takibi (`.beyin-version`) ve `scripts/upgrade.ps1` betiği ile notlarınıza ve hafızanıza dokunmadan sistem dosyalarını tek komutla güncelleyebilirsiniz.
* **🔒 Eşzamanlılık & Güvenlik:** `portalocker` dosya kilitleme mekanizması sayesinde çoklu alt ajanlar ve arka plan cron görevleri güvenle çalışır.

---

## 🚀 Tek Komutla Hızlı Kurulum

Google Antigravity 2.0 çalışma alanınızda şu komutu verin:

```text
Read beyin-antigravity.md and build the second brain system in this workspace. When finished, report all installed components.
```

Sistem durumunu istediğiniz zaman denetleyin:

```bash
python .agents/scripts/doctor.py
# Veya Antigravity sohbetinde: "beyin doktor"
```

---

## 🔄 Synapse-AG Güncelleme

Yeni bir sürüm yayınlandığında kişisel notlarınızı veya hafızanızı kaybetmeden güncelleyin:

```powershell
.\scripts\upgrade.ps1
```

* **Korunan Dizinler (Asla Dokunulmaz):** `daily/`, `knowledge/`, `📥 000-Inbox/`, `🏰 300-Projects/`, `🧠 500-Knowledge/`, `🔮 850-Companion/`, `📦 900-Archive/`
* **Güncellenen Dosyalar:** `.agents/scripts/`, `.agents/hooks.json`, `.obsidian/`, `beyin-antigravity.md`, `GEMINI.md`
* **Otomatik Yedekleme:** Güncelleme öncesi otomatik `.bak-TIMESTAMP/` yedeği alınır.

---

## 💎 Obsidian Entegrasyonu

İkinci beyninizi **[Obsidian](https://obsidian.md)** ile açın:

1. Obsidian uygulamasını açın -> **"Open folder as vault"** seçin.
2. Synapse-AG klasörünüzü (`~/.gemini/antigravity/scratch/synapse-ag/`) seçin.
3. **`Ctrl+G`** tuşuna basarak **İlişki Grafiğini (Graph View)** açın:
   - 🔮 **Mor:** Düşünme Ortağı & Çekirdek Hafıza (`🔮 850-Companion`)
   - 🏰 **Cyan:** Aktif Projeler (`🏰 300-Projects`)
   - 🧠 **Zümrüt Yeşili:** Kalıcı Bilgi & Hata Laboratuvarı (`🧠 500-Knowledge`, `knowledge/`)
   - 📅 **Mavi:** Günlük Oturum Logları (`daily/`)
   - 📥 **Kehribar:** Hızlı Notlar & Inbox (`📥 000-Inbox`)
   - 🎯 **Beyaz:** Kumanda Merkezi & Dashboard (`🎯 100-Command-Center`)

<p align="center">
  <img src="assets/images/obsidian-graph.png" alt="Obsidian Semantik Ağ Grafiği" width="95%" style="border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);" />
</p>

---

## 🏗️ Mimari Yapı

```mermaid
flowchart TD
    subgraph Antigravity ["🧠 Antigravity 2.0 Yaşam Döngüsü"]
        UserPrompt["Kullanıcı İstemi"] --> PreHook["PreInvocation Kancası\n(inject_context.py)"]
        PreHook --> Model["Model & AI Düşünme Ortağı"]
        Model --> StopHook["Stop Kancası\n(flush_daily.py)"]
    end

    subgraph MemoryVault ["📁 Yerel Kasa (%100 Markdown)"]
        Core["🔮 850-Companion\n(Core, Kurallar, Threads, Last-Session)"]
        Daily["📅 daily/YYYY-MM-DD.md"]
        KB["🧠 knowledge/ & 500-Knowledge/\n(Kavramlar, Bağlantılar, Dersler)"]
        Projects["🏰 300-Projects/"]
    end

    subgraph Compiler ["⚙️ Otonom Derleyici (Cron)"]
        Nightly["compile_knowledge.py\n(Bilgi Sentezleyici)"]
    end

    subgraph Obsidian ["💎 Obsidian Masaüstü"]
        GraphView["Graph View (Ctrl+G)\nRenk Kodlu Semantik Ağ"]
        Backlinks["Çift Yönlü [[Wikilinks]]"]
    end

    PreHook -.->|Bağlamı Otomatik Yükler| Core
    StopHook -.->|Oturum Kaydını Ekler| Daily
    Daily --> Nightly
    Nightly -->|Makaleleri Sentezler| KB
    MemoryVault -.->|Yerel Markdown & Graf| Obsidian
```

---

## 📂 Dizin İskeleti

```text
Synapse-AG/
├── LICENSE                         # MIT Lisansı
├── README.md                       # İngilizce Dokümantasyon
├── README_TR.md                    # Türkçe Dokümantasyon
├── beyin-antigravity.md            # Ana Kurulum Şartnamesi
├── GEMINI.md                       # Kök Yönlendirici Kural Dosyası
├── .beyin-version                  # Semantik Sürüm Takibi (2.1.0)
│
├── .obsidian/                      # Hazır Obsidian Ayarları
│   ├── app.json                    # Wikilinks ve Ek Kuralları
│   ├── appearance.json             # AMOLED Koyu Tema
│   ├── core-plugins.json           # Etkin Çekirdek Eklentiler
│   ├── daily-notes.json            # Günlük Not Yönlendirmesi
│   ├── graph.json                  # Renk Kodlu İlişki Grafiği
│   └── templates.json              # Şablon Dizini Yapılandırması
│
├── .agents/                        # Antigravity Kontrol Düzlemi
│   ├── hooks.json                  # Yaşam Döngüsü Kancaları
│   ├── rules/
│   │   └── memory-protocol.md      # Otomatik Yüklenen Hafıza Kuralları
│   ├── skills/
│   │   ├── beyin-doktor/           # Sistem Tanı & Sağlık Denetimi
│   │   ├── hafiza-derleyici/       # Bilgi Tabanı Derleyicisi
│   │   ├── gecmis-import/          # ChatGPT / Claude / Gemini İçe Aktarıcı
│   │   ├── zamanlayici/            # Doğal Dille Zamanlama & Cron
│   │   ├── zaman-yolcusu/          # Git Geçmişi Hafızası
│   │   ├── post-mortem/            # Kök Neden & Hata Laboratuvarı
│   │   └── uzman-ajanlar/          # Uzman Alt Ajanlar
│   └── scripts/
│       ├── _resolve_root.py        # Merkezi Dizin Çözücü
│       ├── inject_context.py       # Bağlam Enjektörü
│       ├── flush_daily.py          # Oturum Loglayıcı
│       ├── compile_knowledge.py    # Bilgi Derleyici
│       └── doctor.py               # Sistem Tanı Betiği
│
├── scripts/
│   └── upgrade.ps1                 # Güvenli Otomatik Güncelleme Betiği
├── tests/
│   └── test_scripts.py             # Pytest Birim Test Paketi
│
├── 📥 000-Inbox/Dump/              # Hızlı Yakalama & Ham Fikirler
├── 🎯 100-Command-Center/          # Dashboard.md & Aktif Öncelikler
├── 🏰 300-Projects/                # Proje Çalışma Alanları
├── 🧠 500-Knowledge/               # Kalıcı Notlar & Lessons.md
├── 🔮 850-Companion/               # Ortak Hafızası (Core, Kurallar, Threads, Last-Session)
├── daily/                          # [Makine Yazar] Günlük Oturum Logları
├── knowledge/                      # [Makine Yazar] Kavramlar ve Bağlantılar
└── 📋 Templates/                   # Not, Proje ve Karar Şablonları
```

---

## 🩺 Tanı & Sağlık Kontrolü (`beyin doktor`)

Sisteminizin sağlık durumunu dilediğiniz an denetleyin:

```bash
python .agents/scripts/doctor.py
```

```text
=================================================================
     ANTIGRAVITY BEYIN DOKTORU RAPORU (v2.1.0)
=================================================================
Bilesen                                          | Durum       
-----------------------------------------------------------------
Kok Yonlendirici (GEMINI.md / beyin-antigravity.md) | [OK] Hazir  
Versiyon Dosyasi (.beyin-version)                | [OK] Hazir  
Antigravity Kancalari (.agents/hooks.json)       | [OK] Hazir  
Baglam Enjektoru (inject_context.py)             | [OK] Hazir  
Oturum Loglayici (flush_daily.py)                | [OK] Hazir  
Bilgi Derleyici (compile_knowledge.py)           | [OK] Hazir  
Obsidian Yapilandirmasi (.obsidian/)             | [OK] Hazir  
Sablon Kasasi (template/)                        | [OK] Hazir  
Git Surum Kontrolu                               | [OK] Git Aktif
=================================================================
[OK] Sistem sapasaglam! Tum hafiza kancalari ve dosyalar hazir.
```

---

## 📜 Lisans & Kaynaklar

Bu proje **[MIT Lisansı](LICENSE)** altında dağıtılmaktadır.

### İlham & Teşekkür:
* **[Avenox](https://avenox.lol)** ([github.com/avenoxai/avenoxbeyin](https://github.com/avenoxai/avenoxbeyin)): İkinci Beyin konsepti ve kanca mimarisi.
* **[Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)**: LLM Bilgi Tabanı ve otonom makale derleme yaklaşımı.
* **[Obsidian](https://obsidian.md)**: Yerel Markdown bilgi grafiği motoru.

---

<p align="center">
  <b>Synapse-AG</b> — Sizinle birlikte büyüyen, kalıcı yapay zeka ikinci beyniniz. 🚀
</p>
