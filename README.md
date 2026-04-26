# 🔥 MXMFOOT - El OSINT más cabrón que SpiderFoot

[![Version](https://img.shields.io/badge/version-1.0.0-red)](https://github.com/Falconmx1/MXMFOOT)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green)](https://python.org)

## ⚡ ¿Qué pedo con MXMFOOT?

MXMFOOT es una herramienta de **OSINT ofensiva** diseñada para ser más rápida, más modular y más perrona que SpiderFoot. Ideal para pentesters, investigadores y curiosos.

## 🚀 Características

- ✅ Enumeración DNS agresiva
- ✅ Scraping web profundo
- ✅ Búsqueda en redes sociales
- ✅ Whois con info completa
- ✅ Motor de módulos extensible
- ✅ Reportes en JSON
- ✅ Banner bien perrón 🤘

## 📦 Instalación

```bash
git clone https://github.com/Falconmx1/MXMFOOT.git
cd MXMFOOT
pip install -r requirements.txt

🎯 Uso
# Escaneo completo
python3 mxmfoot.py -t ejemplo.com

# Módulo específico
python3 mxmfoot.py -t ejemplo.com -m dns

# Guardar reporte
python3 mxmfoot.py -t ejemplo.com -o reporte.json

Comandos de uso final
# Instalación
chmod +x install_ultimate.sh
./install_ultimate.sh

# Configurar API keys
nano config/api_keys.json
# (poner tu OpenAI key, Telegram API, Discord token)

# ATAQUE COMPLETO CON IA
./mxmfoot.sh -t empresaejemplo.com --full-ai

# Solo crawling de Telegram/Discord
./mxmfoot.sh -t empresaejemplo.com --social-crawl

# Solo generación de exploits con IA
./mxmfoot.sh -t empresaejemplo.com --ai-exploit

# Iniciar C2 listener inteligente
./mxmfoot.sh --c2-listener --c2-port 5555
