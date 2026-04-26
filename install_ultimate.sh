#!/bin/bash

echo "💀 MXMFOOT - ULTIMATE AI APOCALYPTIC INSTALLATION 💀"
echo "===================================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 1. Dependencias del sistema
echo -e "${BLUE}[*] Instalando dependencias del sistema...${NC}"
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-venv \
    tor \
    chromium-browser chromium-chromedriver \
    adb android-tools-adb \
    metasploit-framework \
    nmap wireshark \
    build-essential \
    libssl-dev libffi-dev \
    git curl wget

# 2. Configurar TOR
echo -e "${BLUE}[*] Configurando TOR...${NC}"
sudo systemctl enable tor
sudo systemctl start tor

# 3. Crear entorno virtual
echo -e "${BLUE}[*] Creando entorno virtual...${NC}"
python3 -m venv mxmfoot_ai_env
source mxmfoot_ai_env/bin/activate

# 4. Instalar dependencias Python
echo -e "${BLUE}[*] Instalando dependencias Python...${NC}"
pip install --upgrade pip
pip install \
    openai \
    telethon \
    discord.py \
    beautifulsoup4 \
    requests \
    cloudscraper \
    selenium \
    cryptography \
    colorama \
    python-telegram-bot \
    aiohttp \
    stem \
    paramiko \
    pynput \
    flask \
    flask-cors \
    neo4j \
    dnspython \
    whois \
    shodan

# 5. Wordlists para cracking
echo -e "${BLUE}[*] Descargando wordlists...${NC}"
sudo apt install -y wordlists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null

# 6. Estructura de directorios
echo -e "${BLUE}[*] Creando estructura de directorios...${NC}"
mkdir -p reports exploits payloads logs config

# 7. Copiar configuración de ejemplo
if [ ! -f config/api_keys.json ]; then
    echo -e "${YELLOW}[!] Creando configuración de ejemplo...${NC}"
    cat > config/api_keys.json << EOF
{
    "openai_api_key": "TU_API_KEY_AQUI",
    "telegram_api_id": "TU_TELEGRAM_API_ID",
    "telegram_api_hash": "TU_TELEGRAM_API_HASH",
    "discord_token": "TU_DISCORD_TOKEN",
    "shodan_api_key": "TU_SHODAN_API_KEY",
    "github_token": "TU_GITHUB_TOKEN",
    "c2_port": 4444,
    "auto_clean_logs": true,
    "enable_ai": true,
    "max_threads": 10
}
EOF
    echo -e "${YELLOW}[!] EDITAR config/api_keys.json con tus API keys${NC}"
fi

# 8. Script de inicio rápido
echo -e "${BLUE}[*] Creando script de inicio rápido...${NC}"
cat > mxmfoot.sh << 'EOF'
#!/bin/bash
source mxmfoot_ai_env/bin/activate
python3 mxmfoot.py "$@"
EOF
chmod +x mxmfoot.sh

echo -e "${GREEN}[+] INSTALACIÓN COMPLETA${NC}"
echo ""
echo -e "${YELLOW}COMANDOS RÁPIDOS:${NC}"
echo "  ./mxmfoot.sh -t objetivo.com --full-ai     # Ataque completo con IA"
echo "  ./mxmfoot.sh --c2-listener                 # Iniciar C2 listener"
echo "  ./mxmfoot.sh -t objetivo.com --social-crawl # Crawling Telegram/Discord"
echo ""
echo -e "${RED}[!] RECUERDA configurar tus API keys en config/api_keys.json${NC}"
echo -e "${RED}[!] USO ÉTICO Y AUTORIZADO ÚNICAMENTE${NC}"
