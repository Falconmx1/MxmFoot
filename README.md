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

Comando para levantar todo
# Instalar dependencias
pip install -r requirements.txt

# Configurar TOR para dark web (opcional)
sudo apt install tor
sudo systemctl start tor

# Levantar el panel tipo BloodHound
cd web_panel
python app.py

# En otra terminal, correr escaneos CLI
python mxmfoot.py -t ejemplo.com -m all
