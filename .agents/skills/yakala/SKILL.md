---
name: yakala
description: >-
  Tek komutla kaynak yakalar (video, tweet, makale, dosya, pano, not), .ham/ altında izole eder ve 'yakalananları işle' dendiğinde 500-Knowledge/ kalıcı notlarına dönüştürür. "yakala", "beyne at", "yakalananları işle", "kaynak yakala" denildiğinde kullanın.
---

# Yakala Yeteneği

Kullanıcının verdiği bağlantıları, metinleri veya dosyaları tek komutla yakalar ve bekleyen kartları işler.

## Yakalama Adımları:
1. Kullanıcı bir link veya metin verdiğinde:
   `python .agents/scripts/yakala.py "<KAYNAK>" --note "<NEDEN>"`
2. Panodan yakalamak için:
   `python .agents/scripts/yakala.py --clipboard`

## Yakalananları İşleme Adımları:
1. Kullanıcı "yakalananları işle" veya "inbox sentezle" dediğinde:
   `python .agents/scripts/yakala.py process`
2. Kartlar işlendikten sonra yeni oluşturulan veya bağlanan `🧠 500-Knowledge/` notlarını kullanıcıya özetleyin.
