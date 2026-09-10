# Çoklu Ajan ve Hafıza Protokolü

Bu çalışma alanında çalışan tüm ajanlar ve alt ajanlar (subagents) aşağıdaki kurallara tabidir:
1. **Tekil Kaynak İlkesi:** Tüm kalıcı hafıza `850-Companion/` klasöründedir.
2. **Kural Uyumu:** `Kurallar.md` içindeki kurallar her ajan için bağlayıcıdır.
3. **Kendi Başına Varsayım Yapmama:** Bilgi gerekiyorsa önce `knowledge/` veya `500-Knowledge/` altındaki ilgili notu oku.
4. **Merkezi Konum:** Tüm scriptler `SYNAPSE_AG_ROOT` ortam değişkenini veya `.beyin-version` dosyasını kullanarak doğru dizini bulur.
