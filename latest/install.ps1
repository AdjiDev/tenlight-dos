# Function to check if Node.js and npm are installed
function Check-NodeNpm {
    if (Get-Command node -ErrorAction SilentlyContinue) {
        if (Get-Command npm -ErrorAction SilentlyContinue) {
            Write-Host "Node.js and npm are already installed."
            node -v
            npm -v
        } else {
            Write-Host "npm is not installed. Please install it manually."
        }
    } else {
        Write-Host "Node.js is not installed. Please install it manually."
    }
}

# Function to install Node.js and npm using the official installer
function Install-NodeNpm {
    Write-Host "Installing Node.js and npm..."
    Start-Process "https://nodejs.org/en/download/" -UseNewEnvironment
}

# Function to install Python pip module
function Install-All {
    Write-Host "Installing Python requests module..."
    pip install requests
}

# Function to display the main menu and handle user input
function Show-Menu {
    Clear-Host
    Write-Host "Installer Menu"
    Write-Host "==============="
    Write-Host "1. Check if Node.js and npm are installed"
    Write-Host "2. Install Node.js and npm"
    Write-Host "3. Install all and run"
    Write-Host "4. Exit"
    $choice = Read-Host "Please select an option (1-4)"
    
    switch ($choice) {
        "1" {
            Check-NodeNpm
        }
        "2" {
            Install-NodeNpm
        }
        "3" {
            Install-All
        }
        "4" {
            Write-Host "Exiting..."
            exit
        }
        default {
            Write-Host "Invalid option. Please try again."
            Show-Menu
        }
    }
}

# Start the menu loop
Show-Menu
