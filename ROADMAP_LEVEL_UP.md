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

- [x] **Web Tabanlı 3D Bilgi Grafiği (`visualizer/`):** 
  - Three.js & 3D Force-Graph tabanlı interaktif uzay.
  - **🌌 Galaksi Kümeleme Modu (Force-Cluster):** Notların kategorilerine göre ayrı takımyıldızları gibi 3D uzayda kümelenmesi.
  - **🔥 Isı Haritası (Heatmap Glow):** En son çalışılan veya yoğun bağlantılı notların sıcak neon renklerle parlaması.
  - **💾 Tek Tıkla HTML Dışa Aktarma (Export):** Bilgi evrenini tek bir bağımsız HTML dosyası olarak kaydetme.
- [x] **Git Zaman Yolcusu Yeteneği (`zaman-yolcusu` Skill):**
  - Ajanın geçmiş Git commit ve diff kayıtlarını sorgulayabilmesi:  
    *Örnek:* *"2 hafta önce bu mimari kararı neden aldık, hangi dosyaları değiştirdik?"*
- [x] **Hata & Başarısızlık Laboratuvarı (Post-Mortem Engine - `Lessons.md`):**
  - Yaşanan hataların kök neden analiziyle çıkarılan derslerin otomatik olarak `Kurallar.md` ve `Lessons.md` içine işlenmesi.
- [x] **Çoklu Uzman Ajan Sistemi (`uzman-ajanlar` Skill):**
  - Tasarımcı, Güvenlik Denetçisi, Veritabanı Mimarı gibi özel uzman alt ajanların görevlendirilmesi.

---

## 🟠 Level 3: Proaktif & Otonom Ajanlar (Autonomous Living Brain)
*Hedef: Modelin yalnızca siz sorduğunuzda değil, siz yokken de sizin için çalışması.*

- [ ] **Sabah Brifingi Ajanı (Autonomous Morning Digest - Cron):**
  - Her sabah saat 08:00'de otomatik tetiklenen daemon görev.
  - Dünün tamamlanan işlerini, takvimdeki öncelikleri ve `Threads.md` içindeki açık maddeleri derleyip `🎯 100-Command-Center/Bugun.md` sayfasına bırakır.
- [ ] **Hafıza Bahçıvanı (Memory Gardener - Weekly Cron):**
  - Haftada bir çalışan otonom bakım ajanı.
  - Birbirini tekrar eden, çelişen veya yetim kalan (hiçbir yere bağlanmamış) notları tespit eder, birleştirme önerileri hazırlar.
- [ ] **Çoklu Arama (Hybrid Hybrid Search):**
  - Klasik kelime araması (Ripgrep) + Anlamsal vektör araması (mem0 / yerel embedding) ile hibrit hafıza sorgusu.

---

## 🔴 Level 4: Dış Dünya & Çok Kanallı Entegrasyon (Omni-Channel Brain)
*Hedef: İkinci beyninizi her an, her yerden beslemek ve dinlemek.*

- [ ] **Telegram / WhatsApp Hızlı Fikir Yakalama (MCP Webhook):**
  - Dışarıdayken cep telefonunuzdan Telegram botuna attığınız ses kaydı veya hızlı metinlerin doğrudan `📥 000-Inbox/Dump/` içine düşmesi.
- [ ] **Sesli Günlük ve Brifing (Audio Briefing - TTS):**
  - Sabah uyandığınızda veya yürüyüşteyken otonom sabah brifinginizi doğal bir sesle dinletebilen ses motoru entegrasyonu.
- [ ] **Otomatik Web Araştırma İçe Aktarıcısı (Web Ingestion Pipeline):**
  - Beğendiğiniz bir makale veya tweet linkini bıraktığınızda içeriği okuyup, temizleyip, özetleyerek ilgili `500-Knowledge/` klasörüne kaynaklarıyla yerleştiren agentic boru hattı.

---

## 📊 Seviye Matrisi

| Seviye | Adı | İnsan Müdahalesi | Ajan Rolü | Temel Güç |
| :--- | :--- | :--- | :--- | :--- |
| **L1** | Mekanik Hafıza | Yüksek | Reaktif Asistan | Asla unutmama, otomatik oturum logları |
| **L2** | Görsel & Zamansal | Orta | Analitik Ortak | 3D Graph, Galaksi Kümeleme, Isı Haritası, Post-Mortem, Git Zaman Yolculuğu |
| **L3** | Proaktif Beyin | Düşük | Otonom Takım Arkadaşı | Sabah brifingi, hafıza bahçıvanı, cron görevleri |
| **L4** | Çok Kanallı Evren | Sıfır (Dıştan Besleme) | Canlı Zihin | Telegram/Sesli entegrasyon, çoklu kaynak sentezi |
