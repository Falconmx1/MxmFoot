#!/usr/bin/env python3
import shodan
import socket
import json
from colorama import Fore, Style

class ShodanIntel:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.shodan_api = None
        if api_key:
            try:
                self.shodan_api = shodan.Shodan(api_key)
            except:
                pass
    
    def scan_ip(self, target_ip):
        """Escanea una IP con Shodan"""
        results = {
            'host_info': {},
            'open_ports': [],
            'vulnerabilities': [],
            'services': []
        }
        
        if not self.shodan_api:
            return {'error': 'Shodan API key no configurada'}
        
        try:
            host = self.shodan_api.host(target_ip)
            
            results['host_info'] = {
                'ip': host['ip_str'],
                'org': host.get('org', 'N/A'),
                'os': host.get('os', 'N/A'),
                'country': host.get('country_name', 'N/A'),
                'domains': host.get('domains', [])
            }
            
            for service in host.get('data', []):
                port_info = {
                    'port': service['port'],
                    'service': service.get('_shodan', {}).get('module', 'unknown'),
                    'banner': service.get('data', '')[:200]
                }
                results['open_ports'].append(port_info)
                
                # Buscar CVEs
                if 'vulns' in service:
                    for vuln in service['vulns']:
                        results['vulnerabilities'].append({
                            'cve': vuln,
                            'port': service['port']
                        })
            
            return results
            
        except shodan.APIError as e:
            return {'error': str(e)}
    
    def search_domain(self, domain):
        """Busca información del dominio en Shodan"""
        try:
            # Resolver dominio a IP
            ip = socket.gethostbyname(domain)
            return self.scan_ip(ip)
        except:
            return {'error': f'No se pudo resolver {domain}'}
    
    def search_shodan(self, query):
        """Búsqueda avanzada en Shodan"""
        if not self.shodan_api:
            return {'error': 'API key requerida'}
        
        try:
            results = self.shodan_api.search(query, limit=50)
            return {
                'total': results['total'],
                'matches': [
                    {
                        'ip': match['ip_str'],
                        'port': match['port'],
                        'org': match.get('org', 'N/A'),
                        'data': match.get('data', '')[:150]
                    }
                    for match in results['matches']
                ]
            }
        except Exception as e:
            return {'error': str(e)}
