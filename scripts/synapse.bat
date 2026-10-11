@echo off
rem Synapse-AG Windows Master CLI Runner
setlocal
set "SCRIPT_DIR=%~dp0"
set "VAULT_DIR=%SCRIPT_DIR%.."
set "TUI_SCRIPT=%VAULT_DIR%\.agents\scripts\tui.py"
set "YAKALA_SCRIPT=%VAULT_DIR%\.agents\scripts\yakala.py"
set "DOCTOR_SCRIPT=%VAULT_DIR%\.agents\scripts\doctor.py"

where python >nul 2>nul
if %errorlevel%==0 (
    set "PY_CMD=python"
) else (
    set "PY_CMD=py -3"
)

if "%~1"=="" goto run_tui
if /i "%~1"=="tui" goto run_tui
if /i "%~1"=="doctor" goto run_doctor
if /i "%~1"=="doktor" goto run_doctor
if /i "%~1"=="yakala" goto run_yakala
if /i "%~1"=="search" goto run_search
if /i "%~1"=="devil" goto run_devil

%PY_CMD% "%TUI_SCRIPT%" %*
goto end

:run_tui
%PY_CMD% "%TUI_SCRIPT%"
goto end

:run_doctor
%PY_CMD% "%DOCTOR_SCRIPT%"
goto end

:run_yakala
shift
%PY_CMD% "%YAKALA_SCRIPT%" %*
goto end

:run_search
shift
%PY_CMD% "%TUI_SCRIPT%" --search "%~1"
goto end

:run_devil
shift
%PY_CMD% "%TUI_SCRIPT%" --devil "%~1"
goto end

:end
endlocal
