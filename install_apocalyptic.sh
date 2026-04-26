#!/bin/bash

echo "💀 MXMFOOT - INSTALACIÓN APOCALÍPTICA 💀"
echo "========================================="

# 1. Dependencias del sistema
sudo apt update
sudo apt install -y \
    tor \
    chromium-browser \
    chromium-chromedriver \
    adb \
    android-tools-adb \
    android-tools-fastboot \
    jadx \
    metasploit-framework \
    nmap \
    wireshark \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev

# 2. Configurar TOR
sudo systemctl enable tor
sudo systemctl start tor

# 3. Instalar wordlists para cracking
sudo apt install -y wordlists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null

# 4. Instalar Frida para mobile
pip3 install frida-tools
pip3 install androguard

# 5. Descargar YARA rules
git clone https://github.com/Yara-Rules/rules.git /opt/yara-rules

# 6. Configurar entorno Python
python3 -m venv mxmfoot_env
source mxmfoot_env/bin/activate
pip3 install -r requirements.txt

# 7. Configurar base de datos de exploits
cd modules
git clone https://github.com/offensive-security/exploitdb.git exploit-db
cd ..

echo "[+] INSTALACIÓN COMPLETA"
echo "[🔥] MXMFOOT APOCALÍPTICA LISTA"
echo ""
echo "COMANDOS RÁPIDOS:"
echo "  python3 mxmfoot.py -t objetivo.com --full-apocalyptic"
echo "  python3 mxmfoot.py -t objetivo.com --deep-crawl"
echo "  python3 mxmfoot.py -t objetivo.com --zero-day-scan"
echo "  python3 mxmfoot.py --c2-listener --c2-port 5555"
