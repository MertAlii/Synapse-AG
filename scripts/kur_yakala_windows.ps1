# Synapse-AG Windows 'Beyne At' (SendTo) Entegrasyon Kurucusu
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultDir = Split-Path -Parent $ScriptDir
$YakalaScript = Join-Path $VaultDir ".agents\scripts\yakala.py"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "    SYNAPSE-AG WINDOWS 'BEYNE AT' ENTEGRASYONU" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Kasa Dizini: $VaultDir" -ForegroundColor Gray
Write-Host "Yakala Betigi: $YakalaScript" -ForegroundColor Gray

$SendToDir = [Environment]::GetFolderPath("SendTo")
if (-not (Test-Path $SendToDir)) {
    Write-Host "[!] SendTo klasoru bulunamadi: $SendToDir" -ForegroundColor Yellow
    exit 1
}

$BatPath = Join-Path $SendToDir "Beyne At.bat"
$BatLines = @(
    "@echo off",
    "chcp 65001 > nul",
    "set `"SOURCE_FILE=%~1`"",
    "if `"%SOURCE_FILE%`"==`"`" (",
    "    echo [!] Yakalanacak dosya bulunamadi.",
    "    pause",
    "    exit /b 1",
    ")",
    "py -3 `"$YakalaScript`" `"%SOURCE_FILE%`" --note `"Windows Sag Tik ile gonderildi`"",
    "if errorlevel 1 (",
    "    python `"$YakalaScript`" `"%SOURCE_FILE%`" --note `"Windows Sag Tik ile gonderildi`"",
    ")"
)

$BatContent = $BatLines -join "`r`n"
[System.IO.File]::WriteAllText($BatPath, $BatContent, [System.Text.Encoding]::UTF8)

Write-Host "[OK] Windows 'Gonder > Beyne At' menu girdisi eklendi:" -ForegroundColor Green
Write-Host "     -> $BatPath" -ForegroundColor DarkGray
Write-Host "`nKullanim:" -ForegroundColor White
Write-Host "  1. Masaustunde veya herhangi bir klasorde bir dosyaya sag tiklayin." -ForegroundColor Gray
Write-Host "  2. 'Gonder (Send to)' -> 'Beyne At' secin." -ForegroundColor Gray
Write-Host "  3. Dosya aninda 000-Inbox/Yakala/ icine guvenle kaydedilecektir.`n" -ForegroundColor Gray
