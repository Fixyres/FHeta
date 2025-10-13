@echo off
setlocal enabledelayedexpansion

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: This script must be run as administrator
    pause
    exit /b 1
)

set "python_cmd="

echo Finding Python...

for %%p in (python python3 py) do (
    %%p --version >nul 2>&1
    if not errorlevel 1 (
        for /f "tokens=2 delims= " %%v in ('%%p --version 2^>^&1') do (
            for /f "tokens=1 delims=." %%m in ("%%v") do (
                if %%m GEQ 3 (
                    set "python_cmd=%%p"
                    goto :found_python
                )
            )
        )
    )
)

:found_python
if "!python_cmd!"=="" (
    echo Error: Python 3+ is not installed
    pause
    exit /b 1
)

echo Found Python: !python_cmd!
echo Installing...

if not exist "C:\ProgramData\fheta" mkdir "C:\ProgramData\fheta"

where curl >nul 2>&1
if not errorlevel 1 (
    curl -sL "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/embedding.py" -o "C:\ProgramData\fheta\embedding.py"
) else (
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/embedding.py' -OutFile 'C:\ProgramData\fheta\embedding.py' -UseBasicParsing } catch { exit 1 }"
)

if errorlevel 1 (
    echo Error: Failed to download service script
    pause
    exit /b 1
)

if not exist "C:\ProgramData\fheta\embedding.py" (
    echo Error: Failed to download service script
    pause
    exit /b 1
)

echo Creating virtual environment...
!python_cmd! -m venv "C:\ProgramData\fheta\venv"
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

call "C:\ProgramData\fheta\venv\Scripts\activate.bat"

echo Upgrading pip...
pip install --upgrade pip >nul 2>&1
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    pause
    exit /b 1
)

echo Creating startup script...

if not exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup" (
    mkdir "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run """C:\ProgramData\fheta\venv\Scripts\pythonw.exe"" ""C:\ProgramData\fheta\embedding.py""", 0, False
) > "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\hfheta.vbs"

if errorlevel 1 (
    echo Error: Failed to create startup script
    pause
    exit /b 1
)

echo Starting service...

if exist "C:\ProgramData\fheta\venv\Scripts\pythonw.exe" (
    start "" "C:\ProgramData\fheta\venv\Scripts\pythonw.exe" "C:\ProgramData\fheta\embedding.py"
) else (
    start "" /B "C:\ProgramData\fheta\venv\Scripts\python.exe" "C:\ProgramData\fheta\embedding.py"
)

if errorlevel 1 (
    echo Error: Failed to start service
    pause
    exit /b 1
)

timeout /t 3 /nobreak >nul

tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul
if not errorlevel 1 (
    echo Successfully installed and started!
    pause
    exit /b 0
)

tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if not errorlevel 1 (
    echo Successfully installed and started!
    pause
    exit /b 0
)

echo Error: Service failed to start
pause
exit /b 1
