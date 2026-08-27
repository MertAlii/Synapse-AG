---
name: hafiza-derleyici
description: >-
  Günlük oturum loglarını (daily/) analiz eder, Karpathy bilgi mimarisine göre kavram ve bağlantı makaleleri oluşturur/günceller. "hafızayı derle", "bilgi tabanını güncelle", "gece derleyicisi" denildiğinde veya zamanlanmış cron ile çalışır.
---

# Hafıza Derleyici Yeteneği

Bu yetenek, ham günlük kayıtları (`daily/`) yapılandırılmış, bağlantılı bilgi makalelerine (`knowledge/`) dönüştürür.

## Adımlar:
1. `python .agents/scripts/compile_knowledge.py` komutunu çalıştırın.
2. `knowledge/index.md` dosyasının güncellendiğini doğrulayın.
3. Gerekirse yeni kavramlar için `knowledge/concepts/<kavram>.md` dosyalarını zenginleştirin.
