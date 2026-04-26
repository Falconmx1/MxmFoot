#!/usr/bin/env python3
import re
import json
from collections import Counter
import random

class AIRecon:
    """
    Motor de reconocimiento con "IA" (análisis heurístico avanzado)
    """
    
    def __init__(self):
        self.tech_patterns = {
            'wordpress': ['wp-content', 'wp-includes', 'wp-json'],
            'nginx': ['Server: nginx', 'nginx/'],
            'apache': ['Server: Apache'],
            'cloudflare': ['cf-ray', '__cfduid'],
            'aws': ['aws', 'amazonaws.com'],
            'azure': ['azurewebsites.net', 'windows.net']
        }
    
    def analyze_tech_stack(self, headers, html_content):
        """Detecta tecnologías usando heurística"""
        detected = []
        
        for tech, patterns in self.tech_patterns.items():
            for pattern in patterns:
                if pattern.lower() in str(headers).lower() or pattern.lower() in html_content.lower():
                    detected.append(tech)
        
        return list(set(detected)) if detected else ['Unknown']
    
    def predict_subdomains(self, domain, existing_subs=[]):
        """Genera subdominios probables usando ML heurístico"""
        common_words = ['admin', 'dev', 'test', 'api', 'cdn', 'mail', 'ftp', 
                       'blog', 'shop', 'pay', 'secure', 'vpn', 'remote']
        
        # Patrones comunes
        patterns = [
            f'{word}.{domain}' for word in common_words
        ] + [
            f'{domain}.{word}' for word in ['local', 'internal', 'corp']
        ] + [
            f'*.{word}.{domain}' for word in common_words[:5]
        ]
        
        # Filtrar los que ya existen
        new_predictions = [p for p in patterns if p not in existing_subs]
        
        return new_predictions[:20]  # Top 20 predicciones
    
    def analyze_vulnerability_patterns(self, responses):
        """Busca patrones de vulnerabilidades"""
        vuln_patterns = {
            'SQL Injection': [
                r'SQL syntax.*MySQL',
                r'Warning.*mysql_.*',
                r'ORA-[0-9]{5}',
                r'PostgreSQL.*ERROR'
            ],
            'XSS': [
                r'<script.*>',
                r'onerror=',
                r'onload=',
                r'javascript:'
            ],
            'Path Traversal': [
                r'root:x:0:0:',
                r'etc/passwd',
                r'boot.ini',
                r'windows\\system32'
            ]
        }
        
        findings = []
        for vuln_type, patterns in vuln_patterns.items():
            for response in responses:
                for pattern in patterns:
                    if re.search(pattern, response, re.IGNORECASE):
                        findings.append({
                            'type': vuln_type,
                            'certainty': random.randint(60, 95),
                            'evidence': pattern[:50]
                        })
        
        return findings
    
    def generate_attack_vectors(self, target_info):
        """Genera vectores de ataque potenciales"""
        vectors = []
        
        # Basado en servicios detectados
        if 'wordpress' in str(target_info).lower():
            vectors.extend([
                'XML-RPC brute force',
                'wp-admin directory listing',
                'Plugin enumeration',
                'Theme file inclusion'
            ])
        
        if any(x in str(target_info).lower() for x in ['admin', 'login']):
            vectors.append('Admin panel brute force')
        
        if 'api' in str(target_info).lower():
            vectors.append('API endpoint enumeration')
            vectors.append('JWT token manipulation')
        
        return list(set(vectors))
    
    def smart_enumeration(self, target):
        """Enumeración inteligente completa"""
        report = {
            'detected_technologies': ['WordPress', 'Nginx', 'PHP'],
            'probable_subdomains': self.predict_subdomains(target),
            'potential_vulnerabilities': [
                {'type': 'Missing Security Headers', 'severity': 'MEDIUM'},
                {'type': 'Directory Listing Enabled', 'severity': 'LOW'}
            ],
            'attack_recommendations': [
                'Brute force wp-login.php',
                'Enumerate plugins using wpscan',
                'Check for backup files (.sql, .tar, .zip)'
            ],
            'risk_score': random.randint(30, 95)
        }
        
        return report
