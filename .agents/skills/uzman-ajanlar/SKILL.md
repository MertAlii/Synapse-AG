---
name: uzman-ajanlar
description: >-
  Karmaşık projelerde bağımsız alt ajanlar (Tasarımcı, Güvenlik Denetçisi, Veritabanı Mimarı vb.) başlatarak çoklu uzmanlıkla görev yürütür. "uzman ajan çalıştır", "güvenlik denetimi", "tasarımcı gözüyle bak", "alt ajan ata" denildiğinde kullanın.
---

# Çoklu Uzman Ajan Sistemi (Specialist Subagents)

Antigravity 2.0 alt ajan (`invoke_subagent`) yeteneğini kullanarak tek bir genel model yerine özelleşmiş sanal uzmanları devreye sokar.

## Uzman Rolleri:
1. **🎨 UI/UX Tasarımcı Ajanı:** Glassmorphism, Three.js, renk kontrastı ve tipografi standartlarını denetler.
2. **🛡️ Güvenlik Denetçisi Ajanı:** API anahtarı sızıntıları, güvenli olmayan betik çalıştırmaları ve izin kontrollerini yapar.
3. **🗄️ Veritabanı & Bilgi Mimarı Ajanı:** `knowledge/` ve `500-Knowledge/` altındaki veri ilişkilerini, etiket tutarlılığını ve indeksleri optimize eder.
4. **🔍 Kod İncelemeci (Reviewer) Ajanı:** Kod kalitesi, performans ve test kapsamını inceler.

## Adımlar:
- İlgili uzman için `invoke_subagent` aracını çağırın.
- Uzmanın çıktısını alıp `Threads.md` ve ilgili proje klasörüne entegre edin.
