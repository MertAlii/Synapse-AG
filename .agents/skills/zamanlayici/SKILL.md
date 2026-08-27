---
name: zamanlayici
description: >-
  Kullanıcının doğal dille verdiği zamanlama komutlarını (örneğin 'her gün 12:00'de dünü özetle', '30 dakika sonra hatırlat') Antigravity'nin schedule aracına dönüştürür.
---

# Doğal Dil Zamanlayıcı Yeteneği

Kullanıcının "Her gün saat X'te şunu yap" veya "X dakika sonra bana şunu hatırlat" gibi taleplerini Antigravity'nin yerleşik `schedule` aracı ile cron veya one-shot timer'a çevirir.

## Dönüşüm Tablosu:

| Kullanıcı Talebi | `schedule` Parametreleri |
| :--- | :--- |
| "Her gün saat 12:00'de dünün özetini çıkar" | `CronExpression: "0 12 * * *"`, `IsDaemon: true`, `Prompt: "daily/ notlarını tara ve bugünün özetini çıkar"` |
| "Her akşam 18:00'de hafızayı derle" | `CronExpression: "0 18 * * *"`, `IsDaemon: true`, `Prompt: "hafiza-derleyici yeteneğini çalıştır"` |
| "30 dakika sonra durum kontrolü yap" | `DurationSeconds: 1800`, `TimerCondition: "never"`, `Prompt: "Durum kontrolü yap ve raporla"` |

## Adımlar:
1. İfadeden saat ve periyodu çıkartın.
2. `schedule` aracını uygun parametrelerle çağırın.
3. Kullanıcıya görevin arka planda zamanlandığını teyit edin.
