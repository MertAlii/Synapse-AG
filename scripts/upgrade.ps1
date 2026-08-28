# Synapse-AG Upgrade Script (Antigravity 2.0 & Obsidian)
param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/MertAlii/Synapse-AG"
$RAW_BASE = "https://raw.githubusercontent.com/MertAlii/Synapse-AG/main"

# Korunan dizinler - Kullanici verilerine ASLA dokunulmaz
$PROTECTED_PATTERNS = @(
    "daily",
    "knowledge",
    "*000-Inbox*",
    "*300-Projects*",
    "*500-Knowledge*",
    "*850-Companion*",
    "*900-Archive*"
)

# Sistem dosyalari - Guncellenir
$SYSTEM_FILES = @(
    ".agents/scripts/_resolve_root.py",
    ".agents/scripts/flush_daily.py",
    ".agents/scripts/inject_context.py",
    ".agents/scripts/compile_knowledge.py",
    ".agents/scripts/doctor.py",
    ".agents/hooks.json",
    ".agents/rules/memory-protocol.md",
    ".obsidian/app.json",
    ".obsidian/core-plugins.json",
    ".obsidian/graph.json",
    ".obsidian/daily-notes.json",
    ".obsidian/templates.json",
    ".obsidian/appearance.json",
    "beyin-antigravity.md",
    "GEMINI.md",
    ".beyin-version"
)

function Get-SynapseRoot {
    $scriptDir = Split-Path -Parent $PSScriptRoot
    if (Test-Path (Join-Path $scriptDir ".beyin-version")) {
        return $scriptDir
    }
    
    $current = Get-Location
    while ($current) {
        if (Test-Path (Join-Path $current ".beyin-version")) {
            return $current.Path
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
    
    $default = Join-Path $env:USERPROFILE ".gemini\antigravity\scratch\synapse-ag"
    if (Test-Path (Join-Path $default ".beyin-version")) {
        return $default
    }
    
    Write-Error "Synapse-AG kok dizini bulunamadi! .beyin-version dosyasi araniyor."
    exit 1
}

function Get-RemoteVersion {
    try {
        $wc = New-Object System.Net.WebClient
        $wc.Encoding = [System.Text.Encoding]::UTF8
        $content = $wc.DownloadString("$RAW_BASE/.beyin-version")
        return $content.Trim()
    }
    catch {
        Write-Warning "Uzak surum alinamadi (internet baglantisi yok veya offline)."
        return $null
    }
}

function New-Backup {
    param([string]$Root)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    $backupDir = Join-Path $Root ".bak-$timestamp"
    
    Write-Host "Yedek olusturuluyor: $backupDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    foreach ($file in $SYSTEM_FILES) {
        $source = Join-Path $Root $file
        if (Test-Path $source) {
            $dest = Join-Path $backupDir $file
            $destDir = Split-Path -Parent $dest
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item -LiteralPath $source -Destination $dest -Force
        }
    }
    
    Write-Host "  Yedek tamamlandi." -ForegroundColor Green
    return $backupDir
}

function Update-SystemFiles {
    param([string]$Root)
    
    $updated = 0
    $failed = 0
    $wc = New-Object System.Net.WebClient
    $wc.Encoding = [System.Text.Encoding]::UTF8
    
    foreach ($file in $SYSTEM_FILES) {
        $url = "$RAW_BASE/$file"
        $dest = Join-Path $Root $file
        $destDir = Split-Path -Parent $dest
        
        try {
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            if ($DryRun) {
                Write-Host "  [DRY RUN] Guncellenecek: $file" -ForegroundColor Yellow
            }
            else {
                $content = $wc.DownloadString($url)
                [System.IO.File]::WriteAllText($dest, $content, [System.Text.Encoding]::UTF8)
                Write-Host "  [OK] $file" -ForegroundColor Green
            }
            $updated++
        }
        catch {
            Write-Host "  [ERR] $file -> $_" -ForegroundColor Red
            $failed++
        }
    }
    
    return @{ Updated = $updated; Failed = $failed }
}

function Invoke-PostUpdate {
    param([string]$Root)
    
    $compileScript = Join-Path $Root ".agents\scripts\compile_knowledge.py"
    if (Test-Path $compileScript) {
        Write-Host "Bilgi tabani indeksi yenileniyor..." -ForegroundColor Cyan
        try {
            $env:SYNAPSE_AG_ROOT = $Root
            & python $compileScript 2>$null
            Write-Host "  [OK] Bilgi tabani indeksi guncellendi." -ForegroundColor Green
        }
        catch {
            Write-Host "  [!] Bilgi tabani derlenemedi." -ForegroundColor Yellow
        }
    }
}

# --- Ana Akis ---
Write-Host ""
Write-Host "=======================================================" -ForegroundColor Magenta
Write-Host "   SYNAPSE-AG GUNCELLEME ARACI (Antigravity 2.0)" -ForegroundColor White
Write-Host "=======================================================" -ForegroundColor Magenta
Write-Host ""

$root = Get-SynapseRoot
Write-Host "Synapse-AG konumu: $root" -ForegroundColor Cyan

$versionPath = Join-Path $root ".beyin-version"
$currentVersion = "bilinmiyor"
if (Test-Path $versionPath) {
    $currentVersion = (Get-Content -LiteralPath $versionPath -Raw).Trim()
}

$remoteVersion = Get-RemoteVersion

Write-Host "Mevcut surum: $currentVersion" -ForegroundColor White
if ($remoteVersion) {
    Write-Host "Uzak surum:   $remoteVersion" -ForegroundColor White
}
else {
    Write-Host "Uzak surum:   alinamadi" -ForegroundColor Yellow
}
Write-Host ""

if ($remoteVersion -and $currentVersion -eq $remoteVersion -and -not $Force) {
    Write-Host "Zaten guncelsiniz! (v$currentVersion)" -ForegroundColor Green
    Write-Host "Zorla guncellemek icin: .\scripts\upgrade.ps1 -Force" -ForegroundColor Gray
    exit 0
}

Write-Host "Korunan kullanici verileri:" -ForegroundColor Green
foreach ($p in $PROTECTED_PATTERNS) {
    Write-Host "  [KORUNDU] $p" -ForegroundColor Gray
}
Write-Host ""

if (-not $DryRun -and -not $Force) {
    $confirm = Read-Host "Guncellemeye devam edilsin mi? (e/h)"
    if ($confirm -notin @("e", "E", "evet", "yes", "y")) {
        Write-Host "Iptal edildi." -ForegroundColor Yellow
        exit 0
    }
}

$backupDir = New-Backup -Root $root

Write-Host ""
Write-Host "Sistem dosyalari guncelleniyor..." -ForegroundColor Cyan
$result = Update-SystemFiles -Root $root

if (-not $DryRun) {
    Invoke-PostUpdate -Root $root
}

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Magenta
if ($DryRun) {
    Write-Host "   [DRY RUN] Guncelleme simulasyonu tamamlandi." -ForegroundColor Yellow
}
else {
    Write-Host "   [OK] GUNCELLEME TAMAMLANDI!" -ForegroundColor Green
}
Write-Host "=======================================================" -ForegroundColor Magenta
Write-Host "   Guncellenen: $($result.Updated) dosya" -ForegroundColor White
Write-Host "   Basarisiz:   $($result.Failed) dosya" -ForegroundColor $(if ($result.Failed -gt 0) { "Red" } else { "White" })
Write-Host "   Yedek:       $backupDir" -ForegroundColor Gray
Write-Host ""
