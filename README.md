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

Comandos de uso
# Escaneo completo con cadena de ataque
python3 mxmfoot.py -t empresaejemplo.com --full-attack

# Solo C2 listener
python3 mxmfoot.py -t 0.0.0.0 --c2-listener --c2-port 5555

# Buscar leaks en GitHub
python3 mxmfoot.py -t empresaejemplo.com --github-leaks

# Recon en Telegram/Discord
python3 mxmfoot.py -t nombre_usuario --social-recon

# Auto-exploit con MSF
python3 mxmfoot.py -t 192.168.1.100 --auto-exploit

# Exportar todo a Neo4j para análisis tipo BloodHound
python3 mxmfoot.py -t empresaejemplo.com --neo4j-export

# Desactivar auto-delete de logs (debug)
python3 mxmfoot.py -t empresaejemplo.com --no-clean
