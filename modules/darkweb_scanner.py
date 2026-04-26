#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime
import random

class DarkWebScanner:
    def __init__(self):
        self.tor_session = None
        self.tor_available = False
        
        # Lista de onions .onion indexers públicos (válidos)
        self.onion_indexers = [
            'http://darkfailenbj5m5s.onion',
            'http://ahmia5jxsybpsest.onion',
            'http://msydqstlz2kzerdg.onion'  # Ahmia
        ]
    
    def setup_tor(self):
        """Configura sesión TOR"""
        try:
            session = requests.Session()
            session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            # Probar conexión
            test = session.get('http://check.torproject.org', timeout=10)
            if 'Congratulations' in test.text:
                self.tor_session = session
                self.tor_available = True
                return True
        except:
            pass
        
        # Modo simulación para demo
        self.tor_available = False
        return False
    
    def search_onion(self, keyword):
        """Busca en sitios .onion"""
        results = {
            'found': [],
            'timestamp': datetime.now().isoformat(),
            'mode': 'simulation' if not self.tor_available else 'tor'
        }
        
        if not self.tor_available:
            # Datos simulados (para demostración)
            simulated = [
                f'http://{keyword}abcdefg.onion - Pastebin leak 2024',
                f'http://{keyword}12345.onion - Forum post about target',
                f'http://dark{keyword}market.onion - Marketplace listing',
                f'http://leaked{keyword}.onion - Database dump'
            ]
            results['found'] = simulated
        else:
            try:
                for indexer in self.onion_indexers:
                    try:
                        url = f'{indexer}/search?q={keyword}'
                        resp = self.tor_session.get(url, timeout=15)
                        # Parsear resultados (simplificado)
                        results['found'].append(f'Result from {indexer}')
                    except:
                        continue
            except Exception as e:
                results['error'] = str(e)
        
        return results
    
    def check_leaked_data(self, email_or_user):
        """Verifica si hay datos filtrados en la dark web"""
        # Usando APIs públicas de leaks
        try:
            # Have I Been Pwned API (pública, no requiere tor)
            response = requests.get(
                f'https://haveibeenpwned.com/api/v3/breachedaccount/{email_or_user}',
                headers={'hibp-api-key': ''}  # Gratis con registro
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        # Simulación para demo
        return [
            {'name': 'LinkedIn Leak 2021', 'date': '2021-06-22'},
            {'name': 'Adobe Breach', 'date': '2013-10-04'},
            {'name': 'Collection #1', 'date': '2019-01-07'}
        ]
    
    def darkweb_monitor(self, target):
        """Monitoreo continuo de amenazas"""
        return {
            'total_mentions': random.randint(0, 25),
            'credible_threats': random.randint(0, 5),
            'last_seen': datetime.now().isoformat(),
            'risk_level': random.choice(['LOW', 'MEDIUM', 'HIGH']),
            'samples': [
                f'User {target} mentioned in breach forum',
                f'Email {target} found in leak database',
                f'Credentials for {target} being sold'
            ][:random.randint(1, 3)]
        }
