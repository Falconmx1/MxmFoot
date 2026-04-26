#!/usr/bin/env python3
import requests
import re
import json
import base64
from datetime import datetime
from colorama import Fore

class GitHubLeaks:
    def __init__(self, github_token=None):
        self.token = github_token
        self.headers = {'Authorization': f'token {github_token}'} if github_token else {}
        self.base_url = "https://api.github.com"
        
    def search_leaks(self, keyword, max_results=50):
        """Busca leaks en GitHub"""
        print(f"{Fore.BLUE}[*] Buscando leaks en GitHub para: {keyword}{Style.RESET_ALL}")
        
        patterns = {
            'API Keys': r'[A-Za-z0-9_]{32,45}',
            'AWS Keys': r'AKIA[0-9A-Z]{16}',
            'GitHub Tokens': r'gh[pous]_[0-9A-Za-z]{36}',
            'Cloudflare Keys': r'[0-9a-f]{37}',
            'Database Passwords': r'password[\s]*[:=][\s]*[\'"]?[^\'"]+[\'"]?',
            'JWT Tokens': r'eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
            'SSH Keys': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
            'Slack Tokens': r'xox[baprs]-[0-9A-Za-z-]{10,48}',
            'Google API': r'AIza[0-9A-Za-z-_]{35}',
            'MongoDB': r'mongodb(?:\+srv)?:\/\/[^\s]+'
        }
        
        results = {'total': 0, 'leaks': {}}
        
        # Búsqueda en código
        query = f'{keyword} in:file extension:txt extension:json extension:env extension:yml extension:py extension:js extension:php'
        
        url = f"{self.base_url}/search/code"
        params = {'q': query, 'per_page': min(max_results, 100)}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results['total'] = data.get('total_count', 0)
                
                for item in data.get('items', []):
                    file_url = item['html_url']
                    content = self.get_file_content(item['url'])
                    
                    # Analizar contenido
                    for leak_type, pattern in patterns.items():
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            if leak_type not in results['leaks']:
                                results['leaks'][leak_type] = []
                            
                            results['leaks'][leak_type].append({
                                'file': file_url,
                                'matches': matches[:3],
                                'repo': item['repository']['full_name']
                            })
            else:
                results['error'] = f"GitHub API error: {response.status_code}"
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def get_file_content(self, url):
        """Obtiene contenido de un archivo"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                content = response.json().get('content', '')
                return base64.b64decode(content).decode('utf-8', errors='ignore')
        except:
            pass
        return ''
    
    def search_gist_leaks(self, keyword):
        """Busca en Gists (más común para leaks)"""
        url = f"{self.base_url}/gists/public"
        params = {'since': datetime.now().strftime('%Y-%m-%d')}
        
        leaks_found = []
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                gists = response.json()
                
                for gist in gists[:50]:
                    if keyword.lower() in str(gist).lower():
                        for file_name, file_data in gist['files'].items():
                            if file_data.get('content'):
                                # Buscar patrones de leaks
                                if re.search(r'(password|token|key|secret)', file_data['content'], re.IGNORECASE):
                                    leaks_found.append({
                                        'gist_url': gist['html_url'],
                                        'file': file_name,
                                        'description': gist.get('description', 'No description'),
                                        'owner': gist['owner']['login']
                                    })
        except:
            pass
        
        return leaks_found
    
    def monitor_organization(self, org_name):
        """Monitorea leaks en organización específica"""
        url = f"{self.base_url}/orgs/{org_name}/repos"
        
        try:
            response = requests.get(url, headers=self.headers)
            repos = response.json()
            
            results = []
            for repo in repos[:20]:
                # Verificar commits sospechosos
                commits_url = f"{self.base_url}/repos/{org_name}/{repo['name']}/commits"
                commits_resp = requests.get(commits_url, headers=self.headers)
                
                if commits_resp.status_code == 200:
                    for commit in commits_resp.json()[:10]:
                        if 'key' in commit['commit']['message'].lower() or 'password' in commit['commit']['message'].lower():
                            results.append({
                                'repo': repo['name'],
                                'commit': commit['html_url'],
                                'message': commit['commit']['message']
                            })
            
            return results
        except:
            return []
