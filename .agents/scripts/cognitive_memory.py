#!/usr/bin/env python3
"""
Synapse-AG Çift Katmanlı Bilişsel Hafıza (cognitive_memory.py)
-----------------------------------------------------------
Hipokampüs (Kısa Vadeli Hafıza) ⇄ Neokorteks (Uzun Vadeli Hafıza)
Ebbinghaus Unutma Eğrisi & Aralıklı Pekiştirme (Spaced Reinforcement) Motoru.
"""
import os
import sys
import math
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, safe_write

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ebbinghaus varsayılan parametreleri
DEFAULT_HIPPOCAMPUS_STABILITY = 7.0     # Gün
DEFAULT_NEOCORTEX_STABILITY = 90.0      # Gün
STABILITY_GROWTH_FACTOR = 1.5           # Her pekiştirmede kararlılık artış çarpanı

def calculate_ebbinghaus_retention(delta_days, stability):
    """Ebbinghaus unutma formülü: R = e^(-t / S)"""
    if stability <= 0:
        return 0.0
    return math.exp(-max(0.0, float(delta_days)) / float(stability))

def classify_layer(rel_path):
    """Dosya yoluna göre bilişsel katmanı belirler."""
    norm = rel_path.replace("\\", "/").lower()
    if any(norm.startswith(p) for p in ["daily/", "000-inbox/", "📥 000-inbox/"]):
        return "hippocampus"
    elif any(norm.startswith(p) for p in ["500-knowledge/", "🧠 500-knowledge/", "knowledge/", "850-companion/kurallar"]):
        return "neocortex"
    return "intermediate"

def load_cognitive_state(root):
    state_file = root / ".agents" / "scripts" / ".state" / "cognitive_state.json"
    if state_file.exists():
        try:
            return json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"items": {}, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def save_cognitive_state(root, state):
    state_file = root / ".agents" / "scripts" / ".state" / "cognitive_state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_write(state_file, json.dumps(state, ensure_ascii=False, indent=2), mode="w")

def scan_and_update_vault(root=None):
    """Kasadaki notları tarar ve bilişsel hafıza durumunu yeniler."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    state = load_cognitive_state(root)
    now = datetime.now()
    known_items = state.get("items", {})

    target_dirs = [
        root / "daily",
        root / "000-Inbox",
        root / "📥 000-Inbox",
        root / "500-Knowledge",
        root / "🧠 500-Knowledge",
        root / "knowledge",
        root / "850-Companion"
    ]

    for tdir in target_dirs:
        if not tdir.exists():
            continue
        for p in tdir.rglob("*.md"):
            parts = p.parts
            if any(skip in parts for skip in [".git", "node_modules", ".venv", "venv", ".bak", ".ham"]):
                continue

            rel_p = str(p.relative_to(root)).replace("\\", "/")
            layer = classify_layer(rel_p)

            mtime = datetime.fromtimestamp(p.stat().st_mtime)
            
            if rel_p not in known_items:
                base_stability = DEFAULT_NEOCORTEX_STABILITY if layer == "neocortex" else DEFAULT_HIPPOCAMPUS_STABILITY
                known_items[rel_p] = {
                    "layer": layer,
                    "created_at": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_accessed": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                    "reinforcements": 0,
                    "stability_days": base_stability,
                    "cognitive_weight": 1.0 if layer == "neocortex" else 0.8
                }
            else:
                # Katman güncelliğini koru
                known_items[rel_p]["layer"] = layer

    # Retention skorlarını hesapla
    for rel_p, data in known_items.items():
        try:
            last_dt = datetime.strptime(data.get("last_accessed", ""), "%Y-%m-%d %H:%M:%S")
        except Exception:
            last_dt = now - timedelta(days=1)

        delta_days = (now - last_dt).total_seconds() / 86400.0
        stability = data.get("stability_days", DEFAULT_HIPPOCAMPUS_STABILITY)
        retention = calculate_ebbinghaus_retention(delta_days, stability)
        
        # Bilişsel ağırlık = Katman tabanı * (1 + 0.2 * pekiştirme) * retansiyon
        layer_mult = 1.5 if data.get("layer") == "neocortex" else 1.0
        weight = layer_mult * (1.0 + 0.25 * data.get("reinforcements", 0)) * (0.3 + 0.7 * retention)

        data["delta_days"] = round(delta_days, 1)
        data["retention_score"] = round(retention, 3)
        data["cognitive_weight"] = round(weight, 3)

    state["items"] = known_items
    save_cognitive_state(root, state)
    return state

def reinforce_memory(rel_path, root=None):
    """Bir notu aralıklı pekiştirme (Spaced Reinforcement) ile güçlendirir."""
    if root is None:
        root = resolve_root()
    root = Path(root)

    state = load_cognitive_state(root)
    items = state.get("items", {})
    norm_path = rel_path.replace("\\", "/")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if norm_path not in items:
        # Yeni ekle
        layer = classify_layer(norm_path)
        base_stability = DEFAULT_NEOCORTEX_STABILITY if layer == "neocortex" else DEFAULT_HIPPOCAMPUS_STABILITY
        items[norm_path] = {
            "layer": layer,
            "created_at": now_str,
            "last_accessed": now_str,
            "reinforcements": 1,
            "stability_days": base_stability * STABILITY_GROWTH_FACTOR,
            "retention_score": 1.0,
            "cognitive_weight": 1.5
        }
    else:
        entry = items[norm_path]
        entry["last_accessed"] = now_str
        entry["reinforcements"] = entry.get("reinforcements", 0) + 1
        entry["stability_days"] = round(entry.get("stability_days", DEFAULT_HIPPOCAMPUS_STABILITY) * STABILITY_GROWTH_FACTOR, 1)
        entry["retention_score"] = 1.0
        layer_mult = 1.5 if entry.get("layer") == "neocortex" else 1.0
        entry["cognitive_weight"] = round(layer_mult * (1.0 + 0.25 * entry["reinforcements"]), 3)

    state["items"] = items
    save_cognitive_state(root, state)
    return items[norm_path]

def get_cognitive_report(root=None):
    """Bilişsel hafıza katmanlarının genel sağlık ve dağılım raporunu döner."""
    state = scan_and_update_vault(root)
    items = state.get("items", {})

    hippo = [v for k, v in items.items() if v.get("layer") == "hippocampus"]
    neocortex = [v for k, v in items.items() if v.get("layer") == "neocortex"]

    # Mezuniyet adayları: Hipokampüste olup >= 3 pekiştirme almışlar
    graduates = [(k, v) for k, v in items.items() if v.get("layer") == "hippocampus" and v.get("reinforcements", 0) >= 3]

    # Unutulma / Arşiv adayları: Retansiyon < 0.20 ve delta_days > 45
    decaying = [(k, v) for k, v in items.items() if v.get("retention_score", 1.0) < 0.20 and v.get("delta_days", 0) > 45]

    avg_hippo_retention = sum(v.get("retention_score", 0) for v in hippo) / max(1, len(hippo))
    avg_neo_retention = sum(v.get("retention_score", 0) for v in neocortex) / max(1, len(neocortex))

    return {
        "hippocampus_count": len(hippo),
        "neocortex_count": len(neocortex),
        "total_count": len(items),
        "avg_hippocampus_retention": round(avg_hippo_retention, 3),
        "avg_neocortex_retention": round(avg_neo_retention, 3),
        "graduation_candidates": graduates,
        "decay_candidates": decaying
    }

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Çift Katmanlı Bilişsel Hafıza Motoru")
    parser.add_argument("action", nargs="?", default="status", choices=["status", "scan", "reinforce", "rank"])
    parser.add_argument("path", nargs="?", default="", help="Pekiştirilecek not yolu (reinforce için)")
    args = parser.parse_args()

    root = resolve_root()

    if args.action == "reinforce":
        if not args.path:
            print("[X] Pekiştirilecek dosya yolunu belirtin.")
            return
        res = reinforce_memory(args.path, root=root)
        print(f"\n[OK] Bellek Pekiştirildi (Spaced Reinforcement):")
        print(f" -> Dosya        : {args.path}")
        print(f" -> Katman       : {res['layer'].upper()}")
        print(f" -> Pekiştirme   : {res['reinforcements']} kez")
        print(f" -> Kararlılık   : {res['stability_days']} gün")
        print(f" -> Bilişsel Skor: {res['cognitive_weight']}\n")
        return

    if args.action in ["status", "scan"]:
        rep = get_cognitive_report(root)
        print("\n=======================================================")
        print("    SYNAPSE-AG BİLİŞSEL HAFIZA RAPORU (EBBINGHAUS)")
        print("=======================================================")
        print(f"🧠 Hipokampüs (Kısa Vadeli) : {rep['hippocampus_count']} not (Ortalama Retansiyon: %{rep['avg_hippocampus_retention']*100:.1f})")
        print(f"🏛️ Neokorteks (Kalıcı/Kural): {rep['neocortex_count']} not (Ortalama Retansiyon: %{rep['avg_neocortex_retention']*100:.1f})")
        print(f"📊 Toplam Bilişsel Varlık   : {rep['total_count']} not")
        print("-------------------------------------------------------")
        print(f"🎓 Mezuniyet Adayları (Kalıcı Bilgiye Dönüştür): {len(rep['graduation_candidates'])} adet")
        for p, d in rep['graduation_candidates'][:3]:
            print(f"   * {p} ({d['reinforcements']} pekiştirme)")
        print(f"🍂 Arşiv Adayları (Unutulma Eşiğinde): {len(rep['decay_candidates'])} adet")
        for p, d in rep['decay_candidates'][:3]:
            print(f"   * {p} (Retansiyon: %{d['retention_score']*100:.1f})")
        print("=======================================================\n")

if __name__ == "__main__":
    main()
