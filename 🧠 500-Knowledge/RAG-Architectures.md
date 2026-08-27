---
title: RAG (Retrieval-Augmented Generation) & Vektör Veritabanları
tags: [rag, vector-db, chromadb, embeddings, on-device]
---
# 🔍 RAG (Retrieval-Augmented Generation) Mimarileri

RAG mimarisi, LLM modellerinin kendi parametrik hafızaları dışındaki harici ve güncel bilgi kaynaklarına dinamik olarak erişmesini sağlayan semantik arama ve üretim altyapısıdır.

## 🔑 Temel Katmanlar
1. **Belge İşleme & Chunking:** Metinlerin, dokümanların ve kod bloklarının anlamsal bütünlükle parçalara bölünmesi.
2. **Embedding & Vektörel Dizinleme:** Metin parçalarının çok boyutlu vektörlere dönüştürülüp ChromaDB / Vector DB üzerinde indekslenmesi.
3. **Semantik Arama (Similarity Search):** Kullanıcı sorgusunun vektör benzerliğiyle (Cosine Similarity / HNSW) en alakalı bağlam parçalarıyla eşleştirilmesi.
4. **On-Device / Yerel RAG:** Veri gizliliğini korumak amacıyla tüm sürecin cihaz üzerinde (cihaz içi modellerle) işletilmesi.

## 🛠️ İlgili Mert Ali Alkan Projeleri:
- [[VisionRAG]]: Microsoft AI Summer Programı kapsamında geliştirilen; uzun video sahnelerini analiz eden ve cihaz üzerinde çalışan zaman damgalı RAG çözümü.
- [[ThreatIntel-AI]]: 178 MITRE ATT&CK tekniğini barındıran yerel ChromaDB vektör hafızası.
- [[ClarityAI]]: PDF ve el yazılarını Feynman tekniğiyle öğrenme kartlarına dönüştüren çoklu LLM destekli RAG sistemi.
- [[RAG-Contract-Assistant]]: Hukuki ve ticari sözleşmeleri analiz eden RAG asistanı.

## 📚 Bağlantılı Kavramlar:
- [[Agentic-AI]]
- [[Local-LLM-Ollama]]
