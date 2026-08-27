#!/usr/bin/env python3
"""
Antigravity 2.0 Dynamic Graph Compiler
Scans the workspace directories, extracts nodes and links (Obsidian style [[links]]),
and generates visualizer/data.js.
"""
import os
import re
import json
from pathlib import Path
from datetime import datetime

# Group styling configuration
GROUP_CONFIG = {
    "🔮 850-Companion": {"group": "companion", "color": "#a855f7"},
    "🏰 300-Projects": {"group": "projects", "color": "#06b6d4"},
    "🧠 500-Knowledge": {"group": "knowledge", "color": "#10b981"},
    "knowledge": {"group": "knowledge", "color": "#10b981"},
    "daily": {"group": "daily", "color": "#3b82f6"},
    "📥 000-Inbox": {"group": "inbox", "color": "#f59e0b"},
    "🎯 100-Command-Center": {"group": "center", "color": "#ffffff"}
}

def clean_label(stem, group):
    # Add emojis based on group for visual appeal
    emojis = {
        "companion": "🔮 ",
        "projects": "🏰 ",
        "knowledge": "🧠 ",
        "daily": "📅 ",
        "inbox": "📥 ",
        "center": "🎯 "
    }
    emoji = emojis.get(group, "")
    return f"{emoji}{stem}.md" if not stem.endswith((".md", "/")) else f"{emoji}{stem}"

def extract_metadata(file_path):
    desc = "Herhangi bir açıklama girilmemiş."
    activity = 50
    
    # Simple markdown parser for description
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # 1. Look for desc in frontmatter
        fm_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            desc_match = re.search(r"^desc:\s*(.*)$", fm_text, re.MULTILINE)
            if desc_match:
                desc = desc_match.group(1).strip()
            
        # 2. If no frontmatter desc, find first heading or non-empty paragraph
        if desc == "Herhangi bir açıklama girilmemiş.":
            # Remove frontmatter if present
            clean_content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL).strip()
            lines = [l.strip() for l in clean_content.splitlines() if l.strip()]
            for line in lines:
                if line.startswith("#"):
                    # Use title but keep searching for paragraph
                    title = line.lstrip("#").strip()
                    desc = f"'{title}' başlıklı makale."
                elif not line.startswith(("<", "!", "[", "-")):
                    desc = line[:120] + "..." if len(line) > 120 else line
                    break
    except Exception:
        pass
        
    # Calculate activity based on modification time (decaying score)
    try:
        mtime = file_path.stat().st_mtime
        days_ago = (datetime.now() - datetime.fromtimestamp(mtime)).days
        activity = max(30, min(100, 100 - (days_ago * 5)))
    except Exception:
        pass
        
    return desc, activity

def main():
    root = Path(os.getcwd())
    nodes = []
    links = []
    
    # Map from filename stem -> node ID
    stem_to_id = {}
    
    # 1. Scan and register nodes
    for dir_name, config in GROUP_CONFIG.items():
        scan_dir = root / dir_name
        if not scan_dir.exists():
            continue
            
        # Scan all .md files (recursive)
        for file_path in scan_dir.rglob("*.md"):
            stem = file_path.stem
            node_id = stem.replace(" ", "").replace("-", "") # Alpha-numeric ID
            
            # Avoid duplicates
            if node_id in stem_to_id.values():
                continue
                
            rel_path = file_path.relative_to(root).as_posix()
            desc, activity = extract_metadata(file_path)
            
            val = max(10, min(30, int(file_path.stat().st_size / 200))) # Value sized by file content
            
            node = {
                "id": node_id,
                "name": clean_label(file_path.name, config["group"]),
                "path": rel_path,
                "group": config["group"],
                "color": config["color"],
                "val": val,
                "activity": activity,
                "desc": desc
            }
            nodes.append(node)
            stem_to_id[stem.lower()] = node_id
            
    # Add Dashboard node if not present
    dashboard_file = root / "🎯 100-Command-Center" / "Dashboard.md"
    if not dashboard_file.exists():
        # Create a fallback node
        stem_to_id["dashboard"] = "Dashboard"

    # 2. Scan links inside files
    for dir_name, config in GROUP_CONFIG.items():
        scan_dir = root / dir_name
        if not scan_dir.exists():
            continue
            
        for file_path in scan_dir.rglob("*.md"):
            stem = file_path.stem
            source_id = stem_to_id.get(stem.lower())
            if not source_id:
                continue
                
            try:
                content = file_path.read_text(encoding="utf-8")
                # Match [[TargetNode]] or [[TargetNode|alias]]
                matches = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content)
                for target_stem in matches:
                    target_id = stem_to_id.get(target_stem.strip().lower())
                    if target_id and source_id != target_id:
                        # Prevent duplicate links
                        link = {"source": source_id, "target": target_id}
                        if link not in links and {"source": target_id, "target": source_id} not in links:
                            links.append(link)
            except Exception:
                pass

    # Ensure at least some connection to Dashboard if isolated
    for node in nodes:
        if node["id"] != "Dashboard" and not any(l["source"] == node["id"] or l["target"] == node["id"] for l in links):
            # Connect isolated nodes to Dashboard
            links.append({"source": "Dashboard", "target": node["id"]})

    # Write output to visualizer/data.js
    data_js_path = root / "visualizer" / "data.js"
    output_content = f"""// Auto-generated Graph Data by Antigravity compile_graph.py
const rawData = {json.dumps({"nodes": nodes, "links": links}, ensure_ascii=False, indent=2)};
"""
    data_js_path.write_text(output_content, encoding="utf-8")
    print(f"[OK] Graph data compiled successfully to visualizer/data.js ({len(nodes)} nodes, {len(links)} links)")

if __name__ == "__main__":
    main()
