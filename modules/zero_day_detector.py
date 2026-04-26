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
        
        print(f"[+] Cargados {len(exploits)} exploits de Exploit-DB")
        return exploits
    
    def load_heuristic_rules(self):
        """Carga reglas heurísticas YARA"""
        rules = {
            'sql_injection': 'rule SQL_Injection { strings: $sql = /SELECT.*FROM/i $union = /UNION.*SELECT/i condition: $sql or $union }',
            'xss': 'rule XSS { strings: $xss1 = /<script.*>.*<\/script>/ $xss2 = /onerror=.*>/ condition: $xss1 or $xss2 }',
            'path_traversal': 'rule PathTraversal { strings: $dotdot = /\.\.\// $etc = /\/etc\/passwd/ condition: $dotdot or $etc }'
        }
        
        compiled_rules = {}
        for name, rule_text in rules.items():
            try:
                compiled_rules[name] = yara.compile(source=rule_text)
            except:
                pass
        
        return compiled_rules
    
    def analyze_response(self, response_text, request_type='http'):
        """Analiza respuesta en busca de vulnerabilidades 0-day"""
        findings = []
        
        # 1. Análisis con YARA
        for rule_name, rule in self.heuristic_rules.items():
            matches = rule.match(data=response_text)
            if matches:
                findings.append({
                    'type': rule_name,
                    'confidence': 'HIGH',
                    'evidence': matches[0].strings
                })
        
        # 2. Patrones de error inusuales
        error_patterns = [
            (r'SQL (syntax|error).*MySQL', 'SQL Injection'),
            (r'ORA-[0-9]{5}', 'Oracle Error Disclosure'),
            (r'PostgreSQL.*ERROR', 'PostgreSQL Error'),
            (r'\[object\s+Object\]', 'JavaScript Error'),
            (r'Uncaught\s+Exception', 'PHP Error'),
            (r'Fatal\s+error', 'PHP Fatal Error'),
            (r'Notice:\s+Undefined\s+variable', 'PHP Notice'),
            (r'Warning:\s+.*\sfailed', 'PHP Warning'),
            (r'Access denied for user', 'MySQL Auth Error')
        ]
        
        for pattern, vuln_type in error_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                findings.append({
                    'type': vuln_type,
                    'confidence': 'MEDIUM',
                    'pattern': pattern
                })
        
        # 3. Stack traces reveladores
        if 'Traceback' in response_text or 'Stack trace' in response_text:
            stack_trace = re.findall(r'(?:Traceback|Stack trace):(.*?)(?:\n\n|\Z)', response_text, re.DOTALL)
            findings.append({
                'type': 'Information Disclosure',
                'confidence': 'HIGH',
                'data': stack_trace[:500] if stack_trace else response_text[:500]
            })
        
        return findings
    
    def scan_headers(self, headers):
        """Escanea headers HTTP en busca de configuraciones inseguras"""
        issues = []
        
        security_headers = {
            'Strict-Transport-Security': 'HSTS no configurado',
            'Content-Security-Policy': 'CSP no configurado',
            'X-Frame-Options': 'Clickjacking vulnerable',
            'X-Content-Type-Options': 'MIME sniffing permitido',
            'Referrer-Policy': 'Referer leak posible',
            'Permissions-Policy': 'Permisos excesivos'
        }
        
        for header, issue in security_headers.items():
            if header not in headers:
                issues.append(issue)
        
        # Server version disclosure
        if 'Server' in headers and any(v in headers['Server'] for v in ['Apache', 'nginx', 'IIS']):
            issues.append(f"Server version expuesta: {headers['Server']}")
        
        return issues
    
    def detect_unknown_exploit(self, target_info):
        """Detecta posibles 0-days usando ML heurístico"""
        # Análisis de comportamiento
        risk_score = 0
        indicators = []
        
        # 1. Versiones desactualizadas
        if 'version' in target_info:
            old_versions = self.check_version_age(target_info['version'])
            if old_versions:
                risk_score += 30
                indicators.append(f"Versión antigua: {target_info['version']}")
        
        # 2. Patrones conocidos de 0-days
        zero_day_patterns = [
            ('format string', 'Format String Vulnerability'),
            ('heap overflow', 'Heap Overflow'),
            ('use after free', 'Use After Free'),
            ('race condition', 'Race Condition'),
            ('type confusion', 'Type Confusion')
        ]
        
        for pattern, vuln_type in zero_day_patterns:
            if pattern in str(target_info).lower():
                risk_score += 25
                indicators.append(f"Posible 0-day: {vuln_type}")
        
        # 3. Análisis de tráfico anómalo
        if 'anomalies' in target_info:
            risk_score += target_info['anomalies'] * 10
        
        result = {
            'risk_score': min(risk_score, 100),
            'potential_zero_day': risk_score > 70,
            'indicators': indicators,
            'recommendations': []
        }
        
        if result['potential_zero_day']:
            result['recommendations'].append("⚠️ ALERTA: Posible vulnerabilidad 0-day detectada")
            result['recommendations'].append("→ Aislar sistema objetivo")
            result['recommendations'].append("→ Capturar tráfico para análisis forense")
            result['recommendations'].append("→ Reportar a equipo de seguridad")
        
        return result
    
    def check_version_age(self, version):
        """Verifica antigüedad de versión"""
        # En producción, consultar API de fechas de lanzamiento
        import re
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version)
        if match:
            major, minor, patch = map(int, match.groups())
            # Si es muy viejo (ej: versión 1.x o 2.x)
            if major <= 2:
                return True
        return False
    
    def analyze_binary(self, file_path):
        """Analiza binarios en busca de vulnerabilidades"""
        try:
            pe = pefile.PE(file_path)
            
            findings = []
            
            # Verificar secciones sospechosas
            for section in pe.sections:
                if b'UPX' in section.Name or b'packed' in section.Name:
                    findings.append(f"Sección empaquetada: {section.Name}")
            
            # Verificar imports peligrosos
            dangerous_imports = ['system', 'exec', 'popen', 'CreateProcess']
            
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    for imp in entry.imports:
                        if imp.name and any(danger in imp.name.decode().lower() for danger in dangerous_imports):
                            findings.append(f"Función peligrosa importada: {imp.name}")
            
            return findings
        except:
            return []
    
    def predict_exploit(self, vuln_description):
        """Predice exploitabilidad de una vulnerabilidad"""
        # Keywords que indican alta explotabilidad
        high_risk_keywords = ['remote code execution', 'RCE', 'unauthenticated', 
                             'pre-auth', 'zero-click', 'wormable']
        
        # Keywords que indican baja explotabilidad
        low_risk_keywords = ['requires authentication', 'local', 'physical access',
                            'user interaction', 'race condition']
        
        risk_level = 'MEDIUM'
        score = 50
        
        for keyword in high_risk_keywords:
            if keyword.lower() in vuln_description.lower():
                risk_level = 'CRITICAL'
                score = 90
                break
        
        for keyword in low_risk_keywords:
            if keyword.lower() in vuln_description.lower():
                risk_level = 'LOW'
                score = 20
                break
        
        return {
            'exploitability': risk_level,
            'score': score,
            'requires_auth': 'authentication' in vuln_description.lower(),
            'remote': 'remote' in vuln_description.lower() or 'RCE' in vuln_description
        }
