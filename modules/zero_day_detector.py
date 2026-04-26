#!/usr/bin/env python3
import requests
import json
import re
import hashlib
from bs4 import BeautifulSoup
import yara
import pefile
from datetime import datetime

class ZeroDayDetector:
    """Detección automática de vulnerabilidades 0-day"""
    
    def __init__(self):
        self.cve_database = self.load_cve_database()
        self.exploit_database = self.load_exploit_database()
        self.heuristic_rules = self.load_heuristic_rules()
        
    def load_cve_database(self):
        """Carga base de datos de CVEs"""
        cves = {}
        
        # Fuentes de CVE
        sources = [
            'https://cve.circl.lu/api/last',
            'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-recent.json'
        ]
        
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'cve' in str(data):
                        cves.update(data.get('cves', {}))
                    
                    print(f"[+] Cargados {len(cves)} CVEs de {source}")
            except:
                pass
        
        return cves
    
    def load_exploit_database(self):
        """Carga base de datos de exploits conocidos"""
        exploits = []
        
        # Exploit-DB
        try:
            response = requests.get('https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv')
            if response.status_code == 200:
                for line in response.text.split('\n')[1:]:
                    if line:
                        parts = line.split(',')
                        exploits.append({
                            'id': parts[0],
                            'file': parts[1],
                            'description': parts[2],
                            'date': parts[3],
                            'author': parts[4],
                            'type': parts[5],
                            'platform': parts[6],
                            'port': parts[7] if len(parts) > 7 else ''
                        })
        except:
            pass
        
        print(f"[+] Carg
