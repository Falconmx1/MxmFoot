#!/usr/bin/env python3
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse
import socks
import socket
from stem import Signal
from stem.control import Controller
import requests

class DeepWebCrawler:
    """Crawler automático para deep/dark web"""
    
    def __init__(self):
        self.visited_urls = set()
        self.onion_urls = set()
        self.discovered_content = []
        self.tor_session = None
        
    def setup_tor(self):
        """Configura sesión TOR"""
        try:
            session = requests.Session()
            session.proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            self.tor_session = session
            
            # Verificar TOR
            response = session.get('http://check.torproject.org', timeout=10)
            if 'Congratulations' in response.text:
                print("[+] TOR funcionando correctamente")
                return True
        except:
            print("[-] Error conectando a TOR. Asegúrate que Tor esté corriendo")
        
        return False
    
    def crawl_onion(self, start_url, max_urls=100, depth=3):
        """Crawl de sitios .onion"""
        if not self.tor_session:
            if not self.setup_tor():
                return []
        
        print(f"[🕸️] Iniciando crawling deep web: {start_url}")
        
        to_visit = [(start_url, 0)]  # (url, depth)
        
        while to_visit and len(self.visited_urls) < max_urls:
            url, current_depth = to_visit.pop(0)
            
            if url in self.visited_urls or current_depth > depth:
                continue
            
            print(f"[*] Crawleando: {url} (depth {current_depth})")
            self.visited_urls.add(url)
            
            try:
                response = self.tor_session.get(url, timeout=30)
                
                if response.status_code == 200:
                    content = self.extract_content(response.text, url)
                    self.discovered_content.append(content)
                    
                    # Extraer enlaces
                    links = self.extract_links(response.text, url)
                    
                    for link in links:
                        if link not in self.visited_urls and link not in [v[0] for v in to_visit]:
                            if '.onion' in link or self.is_relevant(link):
                                to_visit.append((link, current_depth + 1))
                
                # Rate limiting
                asyncio.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"[-] Error crawling {url}: {e}")
        
        return self.discovered_content
    
    def extract_links(self, html, base_url):
        """Extrae enlaces del HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            full_url = urljoin(base_url, href)
            
            # Limitar a .onion o URLs relevantes
            if '.onion' in full_url or full_url.startswith('http'):
                links.add(full_url)
        
        return links
    
    def extract_content(self, html, url):
        """Extrae contenido relevante"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Eliminar scripts y estilos
        for script in soup(["script", "style"]):
            script.decompose()
        
        content = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'text': soup.get_text(),
            'keywords': self.extract_keywords(soup.get_text()),
            'links': len(self.extract_links(html, url)),
            'timestamp': datetime.now().isoformat()
        }
        
        return content
    
    def extract_keywords(self, text):
        """Extrae palabras clave del texto"""
        # Limpiar texto
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Palabras comunes a ignorar
        stopwords = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'are', 'was'}
        
        # Contar frecuencia
        from collections import Counter
        word_freq = Counter([w for w in words if w not in stopwords])
        
        # Top 10 keywords
        return [word for word, count in word_freq.most_common(10)]
    
    def is_relevant(self, url):
        """Determina si URL es relevante para OSINT"""
        relevant_patterns = [
            r'leak', r'breach', r'database', r'sql', r'credential',
            r'password', r'email', r'dox', r'paste', r'dump'
        ]
        
        for pattern in relevant_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        
        return False
    
    def search_onion_engines(self, query):
        """Busca en motores de búsqueda .onion"""
        engines = {
            'ahmia': 'http://ahmia5jxsybpsest.onion/search/?q={}',
            'torch': 'http://torch66eakd.onion/?q={}',
            'gram': 'http://gram3r5kbm4n2bzn.onion/search?q={}'
        }
        
        results = []
        
        for name, url_template in engines.items():
            try:
                search_url = url_template.format(query)
                response = self.tor_session.get(search_url, timeout=20)
                
                # Parsear resultados específico para cada motor
                if name == 'ahmia':
                    urls = re.findall(r'href="(http[^"]*\.onion[^"]*)"', response.text)
                    results.extend(urls[:10])
                
                print(f"[+] Encontrados {len(urls)} resultados en {name}")
                
            except Exception as e:
                print(f"[-] Error en {name}: {e}")
        
        return list(set(results))
    
    def crawl_darknet_markets(self):
        """Crawlea mercados de la darknet"""
        markets = [
            'http://asap2u4pvplnkzl7.onion',  # ASAP Market
            'http://bohemia5rnlpmhe6.onion',   # Bohemia
            'http://darkowk6b6sztn32.onion'    # Dark0de
        ]
        
        products = []
        
        for market in markets:
            print(f"[*] Escaneando mercado: {market}")
            content = self.crawl_onion(market, max_urls=50, depth=2)
            
            # Extraer productos
            for item in content:
                # Buscar patrones de productos
                if 'price' in item['text'].lower() or '$' in item['text']:
                    products.append(item)
        
        return products
    
    def find_leaked_dbs(self):
        """Busca bases de datos filtradas"""
        dbs = []
        
        # URLs conocidas de leaks
        leak_sites = [
            'http://dowj122broefaxn6.onion',  # LeakBase
            'http://leak7lcrqktdtfb.onion',   # Leaked Data
            'http://6b2i3l4j2lqkyd2m.onion'    # DataLeaks
        ]
        
        for site in leak_sites:
            content = self.crawl_onion(site, max_urls=30)
            
            for item in content:
                if 'database' in item['text'].lower() or 'leak' in item['text'].lower():
                    dbs.append({
                        'source': site,
                        'title': item['title'],
                        'url': item['url'],
                        'preview': item['text'][:500]
                    })
        
        return dbs
