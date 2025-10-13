#!/bin/bash
 
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root"
    exit 1
fi
 
find_python() {
    for cmd in python3 python python3.12 python3.11 python3.10 python3.9; do
        if command -v "$cmd" &> /dev/null; then
            version=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
            major=$(echo "$version" | cut -d. -f1)
            if [ "$major" -ge 3 ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}
 
python_cmd=$(find_python)
 
if [ -z "$python_cmd" ]; then
    echo "Error: Python 3+ is not installed"
    exit 1
fi
 
echo "Found Python: $python_cmd"
echo "Installing..."
 
mkdir -p "$HOME/.fheta"
 
if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
    echo "Error: curl or wget is required"
    exit 1
fi
 
if command -v curl &> /dev/null; then
    curl -sL "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/embedding.py" -o "$HOME/.fheta/embedding.py"
else
    wget -q "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/embedding.py" -O "$HOME/.fheta/embedding.py"
fi
 
if [ $? -ne 0 ] || [ ! -f "$HOME/.fheta/embedding.py" ]; then
    echo "Error: Failed to download service script"
    exit 1
fi
 
echo "Creating virtual environment..."
"$python_cmd" -m venv "$HOME/.fheta/venv"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi
 
source "$HOME/.fheta/venv/bin/activate"
 
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
 
if [ $? -ne 0 ]; then
    echo "Error: Failed to upgrade pip"
    exit 1
fi
 
echo "Creating systemd service..."
 
sudo tee "/etc/systemd/system/hfheta.service" > /dev/null << EOF
[Unit]
Description=Zig hail
After=network.target
 
[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/.fheta
ExecStart=$HOME/.fheta/venv/bin/python $HOME/.fheta/embedding.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
 
[Install]
WantedBy=multi-user.target
EOF
 
if [ $? -ne 0 ]; then
    echo "Error: Failed to create systemd service"
    exit 1
fi
 
sudo systemctl daemon-reload
 
if [ $? -ne 0 ]; then
    echo "Error: Failed to reload systemd daemon"
    exit 1
fi
 
sudo systemctl enable "hfheta" > /dev/null 2>&1
 
if [ $? -ne 0 ]; then
    echo "Error: Failed to enable service"
    exit 1
fi
 
sudo systemctl start "hfheta"
 
if [ $? -ne 0 ]; then
    echo "Error: Failed to start service"
    exit 1
fi
 
sleep 3
 
if sudo systemctl is-active --quiet "hfheta"; then
    echo "Successfully installed and started!"
else
    echo "Error: Service failed to start"
    exit 1
fi
