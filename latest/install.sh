#!/bin/bash

checkNodeNpm() {
    if command -v node &> /dev/null && command -v npm &> /dev/null; then
        echo "Node.js and npm are already installed."
        node -v
        npm -v
    else
        echo "Node.js or npm is not installed."
        installNodeNpm
    fi
}

installNodeNpm() {
    echo "Installing Node.js and npm..."
    os_name=$(checkOs)

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
        exit 1
    fi
}

checkOs() {
    if [ -f /data/data/com.termux/files/usr/bin/bash ]; then
        echo "Termux"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "Unknown"
    fi
}

installModules() {
    echo "Installing required modules..."
    pip install requests
    pip install tabulate
    pip install rich
    pip install bs4
    npm install
}

moveScript() {
    echo "Moving tenlight.py to ~/bin/..."
    mv tenlight.py ~/bin/
    
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo "Adding ~/bin to PATH..."
        export PATH="$HOME/bin:$PATH"
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    fi

    echo "Reloading shell configuration..."
    source ~/.bashrc
    echo "tenlight is now ready!"
    python tenlight.py
}

main() {
    checkNodeNpm
    installModules
    moveScript
    echo "All setup completed successfully."
}

main
