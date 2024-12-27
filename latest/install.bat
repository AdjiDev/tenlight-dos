@echo off
setlocal enabledelayedexpansion

:: Function to check if Node.js and npm are installed
call :checkNodeNpm

:: Function to check Node.js and npm installation
:checkNodeNpm
where node >nul 2>&1
if %errorlevel% equ 0 (
    where npm >nul 2>&1
    if %errorlevel% equ 0 (
        echo Node.js and npm are already installed.
        node -v
        npm -v
    ) else (
        echo npm is not installed. Please install it manually.
    )
) else (
    echo Node.js is not installed. Please install it manually.
)
goto :menu

:: Function to install Node.js and npm using the official installer
:installNodeNpm
echo Installing Node.js and npm...
:: Open the official Node.js download page for Windows
start https://nodejs.org/en/download/
goto :menu

:: Function to install Python pip module
:installAll
npm i
pip install requests

:: Main Menu
:menu
cls
echo Installer Menu
echo ================
echo 1. Check if Node.js and npm are installed
echo 2. Install Node.js and npm
echo 3. Install all and run
echo 4. Exit
set /p choice="Please select an option (1-4): "

if "%choice%"=="1" goto :checkNodeNpm
if "%choice%"=="2" goto :installNodeNpm
if "%choice%"=="3" goto :installAll
if "%choice%"=="4" exit
echo Invalid option. Please try again.
goto :menu
