function Check-NodeNpm {
    if (Get-Command node -ErrorAction SilentlyContinue -and Get-Command npm -ErrorAction SilentlyContinue) {
        Write-Host "Node.js and npm are already installed."
        node -v
        npm -v
    } else {
        Write-Host "Node.js or npm is not installed. Installing..."
        Install-NodeNpm
    }
}

function Install-NodeNpm {
    Write-Host "Installing Node.js and npm..."
    Start-Process "https://nodejs.org/en/download/"
    Write-Host "Please install Node.js and npm manually from the website."
    Write-Host "Once installed, rerun this script."
    exit
}

function Install-Modules {
    Write-Host "Installing required modules..."
    if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
        Write-Host "pip is not installed. Please install Python and pip first."
        Start-Process "https://www.python.org/downloads/"
        exit
    }
    pip install requests
    if (Test-Path "package.json") {
        npm install
    } else {
        Write-Host "No package.json file found. Skipping npm install."
    }
}

function Main {
    Check-NodeNpm
    Install-Modules
    Write-Host "All required modules installed successfully."
}

Main
