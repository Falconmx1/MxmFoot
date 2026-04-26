#!/bin/bash
# quick_start.sh

echo "🔥 MXMFOOT - Ultimate Edition Setup"
echo "===================================="

# Crear estructura de directorios
mkdir -p reports logs modules config web_panel

# Instalar dependencias
pip3 install -r requirements.txt

# Configurar TOR para dark web
sudo apt update
sudo apt install -y tor
sudo systemctl start tor

# Configurar Neo4j con Docker
if ! command -v docker &> /dev/null; then
    echo "Instalando Docker..."
    curl -fsSL https://get.docker.com | sh
fi

docker run -d \
    --name mxmfoot-neo4j \
    -p 7474:7474 -p 7687:7687 \
    -e NEO4J_AUTH=neo4j/mxmfoot2024 \
    neo4j:latest

# Configurar Metasploit
if ! command -v msfconsole &> /dev/null; then
    echo "Instalando Metasploit..."
    curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
    chmod 755 msfinstall
    ./msfinstall
fi

echo "[+] MXMFOOT Ultimate Edition lista!"
echo "    - Panel web: http://localhost:5000"
echo "    - Neo4j: http://localhost:7474 (neo4j/mxmfoot2024)"
echo "    - Ejecutar: python3 mxmfoot.py -t objetivo.com --full-attack"
