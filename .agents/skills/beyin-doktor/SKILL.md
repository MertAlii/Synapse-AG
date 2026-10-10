---
name: beyin-doktor
description: >-
  Antigravity İkinci Beyin sisteminin sağlık durumunu denetler; eksik kancaları, gelen kutusu (Inbox) yaşlanmasını, Git çakışma işaretlerini ve supersedes durumlarını tespit eder. "beyin doktor", "hafıza kontrol", "doktor", "inbox raporu" denildiğinde kullanın.
---

# Beyin Doktoru Pro Yeteneği

Antigravity İkinci Beyin kurulumunun doğruluğunu, kancaların çalışma durumunu, inbox sağlığını ve hafıza kirliliklerini test eder.

## Adımlar:
1. Genel kontrol için:
   `python .agents/scripts/doctor.py`
2. Detaylı gelen kutusu (Inbox) yaşlanma analizi için:
   `python .agents/scripts/doctor.py --inbox-report`
3. Tüm gelişmiş denetimler için:
   `python .agents/scripts/doctor.py --full`
4. Çıktıdaki tanı tablosunu kullanıcıya özetleyin ve varsa aksiyon önerin.
