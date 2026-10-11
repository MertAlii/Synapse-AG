---
title: Öğrenilen Dersler ve Hata Laboratuvarı (Post-Mortem Lab)
updated: 2026-09-10
type: knowledge-base
---
# 🧪 Hata Laboratuvarı & Çıkarılan Dersler (Post-Mortem Engine)

Bu dosya, projelerde veya oturumlarda karşılaşılan hataların, yanlış varsayımların ve krizlerin **kök neden analizini (Root Cause Analysis)** ve çıkarılan **kalıcı kuralları** barındırır.

> "Hata yapmak tecrübedir; aynı hatayı iki kez yapmak sistemsizliktir."

---

## 📊 Dersler Kütüğü

### [DERS-001] 2026-09-10 — İlk Hata Şablonu
- **Karşılaşılan Sorun / Kriz:** (Örn: Modelin var olmayan bir API parametresi varsayması)
- **Kök Neden (5 Neden Analizi):**
  1. *Neden oldu?* Parametre dökümantasyondan teyit edilmedi.
  2. *Neden teyit edilmedi?* Hızlı kod üretme dürtüsü doğrulama refleksinin önüne geçti.
- **Alınan Aksiyon:** Fonksiyon revize edildi, dökümantasyon kütüphanesine eklendi.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"Harici API çağrısı yapmadan önce parametre şemasını resmi dökümandan doğrula."*
- **Etiketler:** `#hata-analizi` `#api` `#dersler`

---

### [DERS-002] 2026-09-20 — Kod Blokları İçindeki Python Yorumlarının Markdown Başlığı Sanılması
- **Karşılaşılan Sorun / Kriz:** Bölüm içi İçindekiler Tablosu (TOC) oluşturulurken Python kod bloklarındaki yorum satırları (`# Train in mixed-precision float16`) doküman başlığı olarak listelendi.
- **Kök Neden:** Markdown metnini satır satır bölüp `/^(#{1,3})\s/` regex'i çalıştırırken kod bloğu açılış/kapanış işaretleri (```` ``` ````) takip edilmedi.
- **Alınan Aksiyon:** `useMemo` içine `inCodeBlock` durum takibi eklendi; kod çiti içindeki hiçbir satır başlık listesine alınmadı. Başlıklardaki `[slug]` sentaksı temizlenip element `id`'sine dönüştürüldü.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"Markdown ayrıştırma veya başlık çıkarma işlemlerinde kod bloğu (fenced code block) bayrağı zorunludur; kod içi yorumlar doküman başlığı sayılamaz."*
- **Etiketler:** `#markdown` `#toc` `#regex` `#nlp2026`

### [DERS-003] 2026-09-20 — Windows IIS Sunucularında SPA Route Yenileme ve Rewrite İhtiyacı
- **Karşılaşılan Sorun / Kriz:** Kullanıcı tarayıcıda sayfayı yenilediğinde veya doğrudan `/admin` gibi bir adrese gittiğinde IIS sunucusu 404 döndürdü.
- **Kök Neden:** Single Page Application (SPA) mimarisinde fiziksel dosya bulunmadığı için Windows IIS istekleri index.html'e yönlendiremedi; sunucu tarafı URL Rewrite kuralı eksikti.
- **Alınan Aksiyon:** `web.config` dosyasına URL Rewrite kuralları eklendi, istemci tarafında da `window.location.hash` (`#/chapter/7.2`, `#/admin`) ile tam senkronize rota takibi sağlandı.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"IIS veya Nginx üzerinde yayınlanan SPA projelerinde mutlak sunucu yönlendirme (URL Rewrite / fallback to index.html) ve istemcide URL state senkronizasyonu eksiksiz kurulmalıdır."*
- **Etiketler:** `#iis` `#spa` `#routing` `#deployment`

### [DERS-004] 2026-09-20 — Teknik Çevirilerde Kısmi Değiştirme (String Replace) Yetersizliği
- **Karşılaşılan Sorun / Kriz:** Bölüm 7.2 Türkçe seçildiğinde metnin %95'i İngilizce kaldı.
- **Kök Neden:** Kod bloklarını korumaya çalışırken metin üzerinde yüzeysel anahtar kelime eşleştirmesi yapıldı; devasa eğitim akışları ve teknik kavramlar çevrilmedi.
- **Alınan Aksiyon:** Bölüm 7.2 (Token Sınıflandırma) baştan sona tam akademik ve mühendislik düzeyinde Türkçe metinle donatıldı; 126 kod bloğu ve değişken eşleşmeleri bozulmadan korundu.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"Akademik ve teknik dökümantasyon çevirilerinde yüzeysel string replace asla kullanılmaz; kavramlar (NER, POS, chunking, word_ids hizalaması vb.) eksiksiz Türkçe anlatım ve orijinal kod bloklarıyla sentezlenir."*
- **Etiketler:** `#nlp` `#localization` `#dataset`

### [DERS-005] 2026-09-21 — React State Bildirim İhmali & ErrorBoundary Koruma Eksikliği
- **Karşılaşılan Sorun / Kriz:** `ReferenceError: sending is not defined` hatası sonucu tüm React bileşen ağacı çöktü, ekran beyaz kaldı ve `/admin` dahil hiçbir sayfaya erişilemedi.
- **Kök Neden:** `RightPresence.jsx` bileşeninde `sending` değişkeni JSX ve form submit içinde kullanılmasına rağmen `useState(false)` bildirimi eksik kaldı. Uygulama kökünde bir ErrorBoundary bulunmadığı için tek bir bileşendeki render hatası tüm siteyi devirdi. Ayrıca backend'de `admin/users` ve `admin/assign-role` rotaları eksikti.
- **Alınan Aksiyon:** 
  1. `RightPresence.jsx` içine `const [sending, setSending] = useState(false);` eklendi.
  2. `main.jsx` etrafına şık bir Apple temalı `ErrorBoundary` eklendi (tek bir widget hatasında bile sitenin çökmesi engellendi).
  3. `api.php`, `public/api.php` ve `server.js` içine `admin/users` ve `admin/assign-role` uç noktaları entegre edildi.
  4. Hem Header profil menüsüne hem Sidebar navigasyonuna doğrudan tıklanabilir `Admin & Rol Masası` butonu yerleştirildi.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"Tüm React projelerinde kök ağaç mutlaka ErrorBoundary ile sarmalanmalı; yeni eklenen form buton durumları (sending, loading vb.) state seviyesinde derleme öncesi taranmalıdır."*
- **Etiketler:** `#react` `#errorboundary` `#state` `#admin` `#resilience`

