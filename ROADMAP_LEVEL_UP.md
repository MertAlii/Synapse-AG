# 🚀 Antigravity Beyin: Level-Up & İleri Düzey Özellikler Yol Haritası

Bu doküman, Antigravity İkinci Beyin projesini basit bir not tutucudan **kendi kendine düşünen, proaktif ve otonom bir AI ortağına** dönüştürecek seviye seviye yol haritasını sunar.

---

## 🟢 Level 1: Temel Mekanizma (Mevcut Sürüm)
*Hedef: Hafızayı bir disiplin olmaktan çıkarıp mekanizmaya dönüştürmek.*

- [x] **PreInvocation Kancası:** Her oturum başında kimlik, aktif iş parçacıkları (`Threads.md`), kurallar ve son oturum özetinin otomatik yüklenmesi.
- [x] **PostInvocation / Stop Kancası:** Oturum kapandığında arka planda `daily/YYYY-MM-DD.md` içine günlük log yazılması.
- [x] **Karpathy Bilgi Derleyicisi:** Günlük logları analiz edip `knowledge/concepts/` ve `knowledge/connections/` makalelerine dönüştüren gece motoru.
- [x] **Obsidian & Saf Local Markdown Uyumu:** %100 yerel, taşınabilir ve kilitlenmesiz dosya yapısı.
- [x] **Temel Git Sürümleme:** Tüm hafızanın anlık Git geçmişi ile güvenceye alınması.
- [x] **Tek Prompt ile Kurulum:** `beyin-antigravity.md` üzerinden tam otomatik kurulum.

---

## 🟡 Level 2: Görselleştirme & Zamansal Bellek (Time Travel)
*Hedef: Geçmişi sorgulanabilir kılmak ve bilginin topolojisini görmek.*

- [x] **Obsidian Yerel İlişki Grafiği (`.obsidian/`):** 
  - Renk kodlu kategorik ilişki grafiği (`Ctrl+G` / Graph View).
  - **🔮 Mor:** Düşünme Ortağı & Çekirdek Hafıza (`🔮 850-Companion`)
  - **🏰 Cyan:** Aktif Projeler (`🏰 300-Projects`)
  - **🧠 Zümrüt Yeşili:** Kalıcı Bilgi & Hata Laboratuvarı (`🧠 500-Knowledge`, `knowledge/`)
  - **📅 Mavi:** Günlük Oturum Logları (`daily/`)
  - **📥 Kehribar:** Hızlı Notlar & Inbox (`📥 000-Inbox`)
  - **🎯 Beyaz:** Kumanda Merkezi & Dashboard (`🎯 100-Command-Center`)
- [x] **Git Zaman Yolcusu Yeteneği (`zaman-yolcusu` Skill):**
  - Ajanın geçmiş Git commit ve diff kayıtlarını sorgulayabilmesi:  
    *Örnek:* *"2 hafta önce bu mimari kararı neden aldık, hangi dosyaları değiştirdik?"*
- [x] **Hata & Başarısızlık Laboratuvarı (Post-Mortem Engine - `Lessons.md`):**
  - Yaşanan hataların kök neden analiziyle çıkarılan derslerin otomatik olarak `Kurallar.md` ve `Lessons.md` içine işlenmesi.
- [x] **Çoklu Uzman Ajan Sistemi (`uzman-ajanlar` Skill):**
  - Tasarımcı, Güvenlik Denetçisi, Veritabanı Mimarı gibi özel uzman alt ajanların görevlendirilmesi.
- [x] **Okapi BM25 & Türkçe Morfolojik Arama (`turkce-bm25-arama` / `search_bm25.py`):**
  - Ünsüz yumuşaması normalizasyonu (kitap/kitabı, örnek/örneği), Wikilink ve başlık öncelikli bilgi yoğunluğu skorlaması.
- [x] **Context Shield & Sıkıştırma Kilidi (`context-shield` / `companion_compact.py`):**
  - 9.500 karakterlik katı bağlam bütçesi, `Kurallar.md` gerekçe budaması, `.beyin-compact.lock` eşzamanlılık kilidi ve aylık otomatik arşivleme.
- [x] **Doctor 2.0 Sağlık Denetimi & Hafıza Hijyeni (`beyin-doktor-pro` / `doctor.py`):**
  - Gelen kutusu (Inbox) yaşlanma raporu, Git çakışma (conflict) marker kontrolü, `supersedes` ve emekli not filtresi.

---

## 🟠 Level 3: Proaktif & Otonom Ajanlar (Autonomous Living Brain)
*Hedef: Modelin yalnızca siz sorduğunuzda değil, siz yokken de sizin için çalışması.*

- [x] **Akıllı Yakalama & Medya İşleme Boru Hattı (`yakala-motoru` / `yakala.py`):**
  - YouTube (transkript/açıklama), Web makalesi, yerel dosya ve pano metinlerini tek tıkla yakalama.
  - `.ham/` klasörüyle arama kirliliğini önleme ve `visibility: private` gizlilik kalkanı.
  - Windows Gezgini sağ tık `Gönder > Beyne At` entegrasyonu (`scripts/kur_yakala_windows.ps1`).
  - Otonom `"yakalananları işle"` boru hattı ile `500-Knowledge/` bağlantıları oluşturma.
- [ ] **Sabah Brifingi Ajanı (Autonomous Morning Digest - Automations):**
  - Her sabah otomatik tetiklenen otomasyon görevi.
  - Dünün tamamlanan işlerini, takvimdeki öncelikleri ve `Threads.md` içindeki açık maddeleri derleyip `🎯 100-Command-Center/Bugun.md` sayfasına bırakır.
- [ ] **Hafıza Bahçıvanı (Memory Gardener - Weekly Automation):**
  - Haftada bir çalışan otonom bakım ajanı.
  - Birbirini tekrar eden, çelişen veya yetim kalan (hiçbir yere bağlanmamış) notları tespit eder, birleştirme önerileri hazırlar.

---

## 🔴 Level 4: Dış Dünya & Çok Kanallı Entegrasyon (Omni-Channel Brain)
*Hedef: İkinci beyninizi her an, her yerden beslemek ve dinlemek.*

- [ ] **Telegram / WhatsApp Hızlı Fikir Yakalama (MCP Webhook):**
  - Dışarıdayken cep telefonunuzdan Telegram botuna attığınız ses kaydı veya hızlı metinlerin doğrudan `📥 000-Inbox/Dump/` içine düşmesi.
- [ ] **Sesli Günlük ve Brifing (Audio Briefing - TTS):**
  - Sabah uyandığınızda veya yürüyüşteyken otonom sabah brifinginizi doğal bir sesle dinletebilen ses motoru entegrasyonu.
- [ ] **Antigravity Yan Panel Canlı UI Uzantısı (UI Extension & Sidecar):**
  - Antigravity 2.0 yan panelinde çalışan canlı interaktif web visualizer paneli.

---

## 📊 Seviye Matrisi

| Seviye | Adı | İnsan Müdahalesi | Ajan Rolü | Temel Güç |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | Mekanik Hafıza | Yüksek | Reaktif Asistan | Asla unutmama, otomatik oturum logları |
| **L2** | Görsel & Zamansal | Orta | Analitik Ortak | 3D Graph, BM25 Türkçe Arama, Context Shield, Doctor 2.0, Post-Mortem, Git Zaman Yolculuğu |
| **L3** | Proaktif Beyin | Düşük | Otonom Takım Arkadaşı | Akıllı Yakala Motoru, Windows SendTo entegrasyonu, sabah brifingi, hafıza bahçıvanı |
| **L4** | Çok Kanallı Evren | Sıfır (Dıştan Besleme) | Canlı Zihin | UI Extension Sidecar, Telegram/Sesli entegrasyon, çoklu kaynak sentezi |
