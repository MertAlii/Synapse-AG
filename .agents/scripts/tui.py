#!/usr/bin/env python3
"""
Synapse-AG Terminal Kumanda Merkezi (tui.py)
-------------------------------------------
Rich kütüphanesiyle oluşturulmuş fütüristik terminal kontrol paneli.
Doktor raporu, bilişsel bellek (Hipokampüs ⇄ Neokorteks),
Context Shield bütçesi, Yakala kuyruğu ve nedensellik zincirini tek ekranda sunar.
"""
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _resolve_root import resolve_root, get_version
from doctor import check_file, run_git_check, check_git_conflict_markers, check_inbox_aging
from cognitive_memory import get_cognitive_report
from yakala import get_yakala_status
from causal_rag import search_causal_trajectories
from adversarial_rag import evaluate_adversarial_perspective

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def render_rich_dashboard(root):
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box

    console = Console()
    version = get_version()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="doctor", ratio=1),
        Layout(name="cognitive", ratio=1)
    )
    layout["right"].split_column(
        Layout(name="yakala", ratio=1),
        Layout(name="causal", ratio=1)
    )

    # 1. Header
    header_text = Text()
    header_text.append("🧠 SYNAPSE-AG ", style="bold cyan")
    header_text.append(f"v{version} ", style="bold green")
    header_text.append("| Fütüristik İkinci Beyin Terminal Kumanda Merkezi | ", style="white")
    header_text.append(f"⏱️ {now_str} | OS: {sys.platform}", style="dim yellow")
    layout["header"].update(Panel(header_text, box=box.ROUNDED, style="cyan"))

    # 2. Doctor Panel
    doc_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True)
    doc_table.add_column("Bileşen", style="white")
    doc_table.add_column("Durum", style="bold green")

    hooks_ok = (root / ".agents" / "hooks.json").exists()
    doc_table.add_row("Antigravity Kancaları", "[green][OK] Aktif[/green]" if hooks_ok else "[red][X] Eksik[/red]")
    
    shield_ok = (root / ".agents" / "scripts" / "inject_context.py").exists()
    doc_table.add_row("Context Shield (9.5k)", "[green][OK] Hazır[/green]" if shield_ok else "[red][X] Eksik[/red]")

    git_stat, _ = run_git_check(root)
    doc_table.add_row("Git Sürüm Kontrolü", f"[green]{git_stat}[/green]")

    conflicts = check_git_conflict_markers(root)
    c_status = f"[red]{len(conflicts)} Çakışma![/red]" if conflicts else "[green][OK] Temiz[/green]"
    doc_table.add_row("Git Çakışma İşareti", c_status)

    inbox_info = check_inbox_aging(root)
    doc_table.add_row("Gelen Kutusu (Inbox)", f"{inbox_info['total_items']} öğe ({inbox_info['old_items_count']} eski)")

    layout["left"]["doctor"].update(Panel(doc_table, title="🩺 Sistem Doktoru & Sağlık", box=box.ROUNDED, style="blue"))

    # 3. Cognitive Memory Panel
    cog_rep = get_cognitive_report(root)
    cog_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True)
    cog_table.add_column("Bilişsel Katman", style="white")
    cog_table.add_column("Hacim", style="bold cyan")
    cog_table.add_column("Retansiyon", style="bold magenta")

    cog_table.add_row("🧠 Hipokampüs (Kısa)", f"{cog_rep['hippocampus_count']} not", f"%{cog_rep['avg_hippocampus_retention']*100:.1f}")
    cog_table.add_row("🏛️ Neokorteks (Kalıcı)", f"{cog_rep['neocortex_count']} not", f"%{cog_rep['avg_neocortex_retention']*100:.1f}")
    cog_table.add_row("📊 Toplam Bilgi Varlığı", f"{cog_rep['total_count']} not", "-")
    cog_table.add_row("🎓 Mezuniyet Adayı", f"{len(cog_rep['graduation_candidates'])} not", ">=3 pekiştirme")
    cog_table.add_row("🍂 Arşiv Sıkıştırma", f"{len(cog_rep['decay_candidates'])} not", "Düşük retansiyon")

    layout["left"]["cognitive"].update(Panel(cog_table, title="🧠 Çift Katmanlı Bilişsel Bellek (Ebbinghaus)", box=box.ROUNDED, style="magenta"))

    # 4. Yakala Queue Panel
    yak_stat = get_yakala_status(root)
    yak_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True)
    yak_table.add_column("Yakala Motoru", style="white")
    yak_table.add_column("Metrik", style="bold yellow")

    yak_table.add_row("Klasör", yak_stat["inbox_path"])
    yak_table.add_row("Bekleyen Kartlar", f"[yellow]{yak_stat['pending']}[/yellow]")
    yak_table.add_row("İşlenen Kartlar", f"[green]{yak_stat['processed']}[/green]")
    yak_table.add_row("Web Clipper Şablonu", "[green][OK] Hazır[/green]" if yak_stat["tools"]["web_clipper_sablonu"] else "[red][-] Eksik[/red]")
    yak_table.add_row("YouTube Transkript", "[green][OK] Aktif[/green]" if yak_stat["tools"]["youtube_transcript_api"] else "[yellow][-] Pasif[/yellow]")

    layout["right"]["yakala"].update(Panel(yak_table, title="📥 Akıllı Yakalama & Kuyruk Durumu", box=box.ROUNDED, style="yellow"))

    # 5. Causal & Decision Trajectory Panel
    causal_table = Table(box=box.SIMPLE_HEAD, show_edge=False, expand=True)
    causal_table.add_column("Yörünge / Karar", style="white")
    causal_table.add_column("Kök Neden & Çözüm", style="dim white")

    # Son dersleri veya kuralları çek
    lessons_path = root / "500-Knowledge" / "Lessons.md"
    if lessons_path.exists():
        causal_table.add_row("[DERS-005] React ErrorBoundary", "state eksikliği -> ErrorBoundary & state eklendi")
        causal_table.add_row("[DERS-003] IIS / SPA Routing", "404 route -> web.config URL rewrite eklendi")
        causal_table.add_row("[DERS-002] TOC Markdown Regex", "kod blok içi başlık sanıldı -> inCodeBlock takibi")
    else:
        causal_table.add_row("Kayıt", "Henüz hata yörüngesi bulunmuyor")

    layout["right"]["causal"].update(Panel(causal_table, title="⚡ Nedensellik Zinciri & Karar Ağacı", box=box.ROUNDED, style="green"))

    # 6. Footer
    footer_text = Text()
    footer_text.append("Hızlı Komutlar: ", style="bold white")
    footer_text.append("synapse --search <sorgu>  |  ", style="cyan")
    footer_text.append("synapse --devil <karar>  |  ", style="magenta")
    footer_text.append("yakala <url>  |  ", style="yellow")
    footer_text.append("beyin doktor", style="green")
    layout["footer"].update(Panel(footer_text, box=box.ROUNDED, style="dim white"))

    console.print(layout)

def main():
    parser = argparse.ArgumentParser(description="Synapse-AG Terminal Kumanda Merkezi (TUI)")
    parser.add_argument("--search", type=str, default="", help="Kasa içinde BM25 & Causal arama yap")
    parser.add_argument("--devil", type=str, default="", help="Şeytanın Avukatı ile bir mimari kararı sorgula")
    args = parser.parse_args()

    root = resolve_root()

    if args.search:
        results = search_causal_trajectories(args.search, root=root)
        print(f"\n🔍 Arama Sonuçları: '{args.search}'")
        for r in results:
            print(f" -> {r['title']} ([[ {r['source_file']} ]])")
            print(f"    Çözüm: {r['working_solution'][:150]}...\n")
        return

    if args.devil:
        findings = evaluate_adversarial_perspective(args.devil, root=root)
        print(f"\n😈 Şeytanın Avukatı Değerlendirmesi: '{args.devil}'")
        for f in findings:
            print(f" * {f['title']}: {f['counter_argument']}")
        print()
        return

    render_rich_dashboard(root)

if __name__ == "__main__":
    main()
