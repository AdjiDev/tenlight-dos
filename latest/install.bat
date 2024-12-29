@echo off
setlocal enabledelayedexpansion

:: Fungsi untuk memeriksa apakah Node.js dan npm sudah terinstal
:CheckNodeNpm
echo Checking if Node.js and npm are installed...
where node >nul 2>&1
if %ERRORLEVEL% equ 0 (
    where npm >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo Node.js and npm are already installed.
        node -v
        npm -v
        goto InstallModules
    ) else (
        echo npm is not installed. Installing Node.js and npm...
        goto InstallNodeNpm
    )
) else (
    echo Node.js is not installed. Installing Node.js and npm...
    goto InstallNodeNpm
)

:: Fungsi untuk menginstal Node.js dan npm
:InstallNodeNpm
echo Opening Node.js download page...
start https://nodejs.org/en/download/
echo Please install Node.js and npm manually, then rerun this script.
pause
exit /b

:: Fungsi untuk menginstal modul Python dan Node.js
:InstallModules
echo Installing required modules...

:: Periksa apakah pip terinstal
where pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo pip is not installed. Please install Python and pip manually.
    start https://www.python.org/downloads/
    pause
    exit /b
)

:: Instal modul Python
pip install requests

:: Instal modul Node.js (jika ada package.json)
if exist package.json (
    npm install
) else (
    echo No package.json found. Skipping npm install.
)

echo All required modules have been installed successfully.
pause
python tenlight.py
