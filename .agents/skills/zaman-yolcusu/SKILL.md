---
name: zaman-yolcusu
description: >-
  Git geçmişini, eski commit mesajlarını ve dosya diff'lerini tarayarak geçmişte alınan kararları ve değişiklikleri araştırır. "geçen hafta neden", "eski kararlar", "git geçmişi", "ne zaman değiştirdik" denildiğinde kullanın.
---

# Git Zaman Yolcusu Yeteneği (Time Travel Memory)

Bu yetenek, kullanıcının geçmişte ne zaman, hangi kararla neyi değiştirdiğini yerel Git geçmişini sorgulayarak açığa çıkarır.

## Kullanım Senaryoları:
- "2 hafta önce bu projenin hedeflerinde neyi değiştirdik?"
- "Bu dosyadaki eski kural neydi?"
- "Son 1 ayda hangi önemli kararlar alındı?"

## Adımlar:
1. `git log --oneline -n 20` veya `git log -p -S "<aranan_kelime>"` ile Git geçmişini tarayın.
2. Değişikliğin yapıldığı commit tarihini, yazarını ve mesajını bulun.
3. Diff içeriğini inceleyerek kullanıcıya kronolojik ve net bir özet sunun.
