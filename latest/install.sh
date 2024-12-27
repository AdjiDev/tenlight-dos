#!/bin/bash

# Function to check if Node.js and npm are installed
checkNodeNpm() {
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        echo "Node.js and npm are already installed."
        node -v
        npm -v
    else
        echo "Node.js or npm is not installed."
    fi
}

# install all
InstallAll() {
    npm i
    pip install requests
    python tenlight.py
}

# Function to install Node.js and npm based on the OS
installNodeNpm() {
    echo "Installing Node.js and npm..."
    os_name=$(CheckOs)

    # Ask for confirmation before installing
    read -p "Do you want to install Node.js and npm? (y/n): " confirmation
    if [[ $confirmation != "y" && $confirmation != "Y" ]]; then
        echo "Installation aborted."
        return
    fi

    case $os_name in
        "Ubuntu" | "Debian")
            sudo apt update
            sudo apt install -y nodejs npm
            ;;

        "Termux")
            pkg update
            pkg install -y nodejs
            ;;

        "Arch" | "Manjaro")
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm nodejs npm
            ;;

        "Fedora" | "RHEL" | "CentOS")
            sudo dnf install -y nodejs npm
            ;;

        "openSUSE")
            sudo zypper install -y nodejs npm
            ;;

        *)
            echo "Unsupported OS. Please install Node.js and npm manually."
            exit 1
            ;;
    esac

    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        echo "Node.js and npm installed successfully."
    else
        echo "Failed to install Node.js and npm."
    fi
}

# Function to check the operating system
CheckOs() {
    if [ -f /data/data/com.termux/files/usr/bin/bash ]; then
        echo "Termux"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "Unknown"
    fi
}

# Main installer menu function
installerMenu() {
    clear
    echo "Installer Menu By ChatGpt"
    echo "==============="
    echo "1. Check if Node.js and npm are installed"
    echo "2. Install Node.js and npm"
    echo "3. Install all and run"
    echo "4. Exit"
    
    read -p "Please select an option (1-4): " choice
    
    case $choice in
        1)
            checkNodeNpm
            ;;
        2)
            installNodeNpm
            ;;
        3)
            InstallAll
            ;;
        4)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            installerMenu
            ;;
    esac
}

# Run the installer menu
installerMenu
