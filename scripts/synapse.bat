@echo off
rem Synapse-AG Windows Master CLI Runner
setlocal
set "SCRIPT_DIR=%~dp0"
set "VAULT_DIR=%SCRIPT_DIR%.."
set "TUI_SCRIPT=%VAULT_DIR%\.agents\scripts\tui.py"
set "YAKALA_SCRIPT=%VAULT_DIR%\.agents\scripts\yakala.py"
set "DOCTOR_SCRIPT=%VAULT_DIR%\.agents\scripts\doctor.py"

if "%~1"=="" goto run_tui
if /i "%~1"=="tui" goto run_tui
if /i "%~1"=="doctor" goto run_doctor
if /i "%~1"=="doktor" goto run_doctor
if /i "%~1"=="yakala" goto run_yakala
if /i "%~1"=="search" goto run_search
if /i "%~1"=="devil" goto run_devil

py -3 "%TUI_SCRIPT%" %*
if errorlevel 1 python "%TUI_SCRIPT%" %*
goto end

:run_tui
py -3 "%TUI_SCRIPT%"
if errorlevel 1 python "%TUI_SCRIPT%"
goto end

:run_doctor
py -3 "%DOCTOR_SCRIPT%"
if errorlevel 1 python "%DOCTOR_SCRIPT%"
goto end

:run_yakala
shift
py -3 "%YAKALA_SCRIPT%" %*
if errorlevel 1 python "%YAKALA_SCRIPT%" %*
goto end

:run_search
shift
py -3 "%TUI_SCRIPT%" --search "%~1"
if errorlevel 1 python "%TUI_SCRIPT%" --search "%~1"
goto end

:run_devil
shift
py -3 "%TUI_SCRIPT%" --devil "%~1"
if errorlevel 1 python "%TUI_SCRIPT%" --devil "%~1"
goto end

:end
endlocal
