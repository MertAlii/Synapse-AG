# 📥 Synapse-AG Akıllı Yakalama Motoru (Yakala)

> **"Gördüğün yerde tek tuşla yakala; ajanın işlesin, dersleri ve çıkarımları kalıcı bilgi ağına bağlasın."**

---

## 💡 Genel Bakış

**Yakala Motoru**, internette gezinirken, araştırma yaparken veya bilgisayar başında çalışırken rastladığınız değerli kaynakları (YouTube videoları, X gönderileri, makaleler, yerel dosyalar veya anlık fikirler) kesintisiz bir şekilde **Synapse-AG** ikinci beyninize aktarmanızı sağlar.

* **🛡️ Sıfır Kirlilik (.ham İzolasyonu):** Ham veriler ve uzun transkriptler `📥 000-Inbox/Yakala/.ham/` altında gizlenir; Obsidian arama sonuçlarını ve not grafiğinizi kirletmez.
* **🔒 Yerel ve Gizlilik Odaklı:** Yakalama anında hiçbir veri dışarıya sızmaz (`visibility: private`). Ağ bağlantısı yalnızca kullanıcının talep ettiği web içeriklerini getirmek için kullanılır.
* **⚡ Tek Tıkla Windows Entegrasyonu:** Herhangi bir dosyaya sağ tıklayıp `Gönder > Beyne At` diyerek doğrudan aktarım yapılabilir.
* **🤖 Otonom İşleme Hattı:** Antigravity içinde `"yakalananları işle"` dediğinizde bekleyen kartlar taranır, temel dersler `🧠 500-Knowledge/` veya `knowledge/concepts/` içine bağlanır.

---

## 🚀 Hızlı Kullanım

### 1. Komut Satırından Yakalama

```bash
# YouTube Videosu Yakalama (Transkript ve açıklama çıkarılır)
python .agents/scripts/yakala.py "https://www.youtube.com/watch?v=..." --note "Yeni LLM mimarisi Ar-Ge incelemesi"

# Web Makalesi veya Araştırma Linki
python .agents/scripts/yakala.py "https://arxiv.org/abs/..." --note "Agentic reasoning makalesi"

# Panodaki Metni Yakalama (Clipboard)
python .agents/scripts/yakala.py --clipboard --note "Hızlı kod parçası"

# Hızlı Düşünce veya Fikir
python .agents/scripts/yakala.py "Gelecek ay NLP projesine yeni bir benchmark ekleyelim"
```

### 2. Windows Gezgini Sağ Tık Entegrasyonu (Gönder > Beyne At)

Kurulumu tek seferlik çalıştırmak yeterlidir:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\kur_yakala_windows.ps1
```
Kurulum tamamlandıktan sonra:
1. Masaüstünde veya herhangi bir klasörde bir dosyaya sağ tıklayın.
2. **Gönder (Send to)** -> **Beyne At** seçeneğine tıklayın.
3. Dosya otomatik olarak `000-Inbox/Yakala/` klasörüne aktarılacaktır.

---

## 🔄 Yakalananları İşleme ("yakalananları işle")

Yakaladığınız ham içerikleri kalıcı bilgiye dönüştürmek için:

**Antigravity Sohbetinde:**
> *"Yakalananları işle"* veya *"Gelen kutusundaki yeni kaynakları sentezle"*

**Komut Satırında:**
```bash
python .agents/scripts/yakala.py process
```

Bu işlem:
1. `status: islenmeyi_bekliyor` durumundaki kartları inceler.
2. Anahtar içgörüleri özetler.
3. `🧠 500-Knowledge/` veya `knowledge/` içinde ilgili kavramlara bağlantı (`[[Wikilink]]`) kurar.
4. Kartı `status: islendi` olarak günceller.

---

## 📂 Dosyalama Yapısı

```text
Synapse-AG/
└── 📥 000-Inbox/
    └── Yakala/
        ├── .ham/                                        # Gizli ham dökümler (aramada görünmez)
        │   └── 20261011_004915_kaynak.ham.txt
        └── 20261011_004915_kaynak.md                    # Obsidian Yakalama Kartı (Frontmatter + Özet)
```
