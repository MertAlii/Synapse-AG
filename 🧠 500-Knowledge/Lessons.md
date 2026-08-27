---
title: Öğrenilen Dersler ve Hata Laboratuvarı (Post-Mortem Lab)
updated: {{TODAY}}
type: knowledge-base
---
# 🧪 Hata Laboratuvarı & Çıkarılan Dersler (Post-Mortem Engine)

Bu dosya, projelerde veya oturumlarda karşılaşılan hataların, yanlış varsayımların ve krizlerin **kök neden analizini (Root Cause Analysis)** ve çıkarılan **kalıcı kuralları** barındırır.

> "Hata yapmak tecrübedir; aynı hatayı iki kez yapmak sistemsizliktir."

---

## 📊 Dersler Kütüğü

### [DERS-001] {{TODAY}} — İlk Hata Şablonu
- **Karşılaşılan Sorun / Kriz:** (Örn: Modelin var olmayan bir API parametresi varsayması)
- **Kök Neden (5 Neden Analizi):**
  1. *Neden oldu?* Parametre dökümantasyondan teyit edilmedi.
  2. *Neden teyit edilmedi?* Hızlı kod üretme dürtüsü doğrulama refleksinin önüne geçti.
- **Alınan Aksiyon:** Fonksiyon revize edildi, dökümantasyon kütüphanesine eklendi.
- **🔮 Kurallar.md'ye Eklenen Kural:** *"Harici API çağrısı yapmadan önce parametre şemasını resmi dökümandan doğrula."*
- **Etiketler:** `#hata-analizi` `#api` `#dersler`

---
