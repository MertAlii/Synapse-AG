---
name: gecmis-import
description: >-
  ChatGPT, Claude veya Gemini dışa aktarımlarını (JSON/HTML/ZIP) yerel olarak parse edip daily/ klasörüne günlük log olarak aktarır. "geçmiş import", "eski sohbetleri aktar", "import chat" denildiğinde kullanın.
---

# Geçmiş İçe Aktarma Yeteneği (Chat Importer)

Kullanıcının eski yapay zeka sohbet geçmişlerini ikinci beynine aktarmasını sağlar. Tüm işlem yerel çalışır, hiçbir yere veri gönderilmez.

## Desteklenen Formatlar:
- ChatGPT `conversations.json`
- Claude `conversations.json`
- Google Gemini dışa aktarımları

## Adımlar:
1. Kullanıcıdan dışa aktarım dosyasının yolunu isteyin.
2. Dosyayı tarihlere göre parçalayarak ilgili `daily/YYYY-MM-DD.md` dosyalarına ekleyin.
3. İçe aktarma bittiğinde `hafiza-derleyici` yeteneğini çalıştırarak indeks oluşturun.
