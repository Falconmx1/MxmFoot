#!/usr/bin/env python3
import random
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import cloudscraper
import tls_client
from urllib.parse import urlparse
import json

class DDoSProtectionBypass:
    """Bypass de Cloudflare, DDoS-Guard, Akamai, etc."""
    
    def __init__(self):
        self.session = None
        self.user_agents = self.load_user_agents()
        self.proxy_list = []
        
    def load_user_agents(self):
        """Carga lista de User-Agents reales"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1'
        ]
    
    def bypass_cloudflare(self, url, max_retries=5):
        """Bypass Cloudflare con diferentes técnicas"""
        print(f"[*] Bypassing Cloudflare para: {url}")
        
        # Técnica 1: Cloudscraper
        try:
            scraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                }
            )
            response = scraper.get(url, timeout=30)
            if response.status_code == 200:
                print("[+] Cloudflare bypass exitoso con cloudscraper")
                return response.text
        except:
            pass
        
        # Técnica 2: TLS Client con fingerprint real
        try:
            client = tls_client.Session(
                client_identifier="chrome_120",
                random_tls_extension_order=True
            )
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            response = client.get(url, headers=headers)
            if response.status_code == 200:
                print("[+] Cloudflare bypass exitoso con TLS fingerprinting")
                return response.text
        except:
            pass
        
        # Técnica 3: Selenium con Chrome headless
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={random.choice(self.user_agents)}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            driver.get(url)
            time.sleep(random.uniform(3, 7))
            
            # Resolver captcha si aparece
            if 'captcha' in driver.page_source.lower():
                print("[!] Captcha detectado, intentando resolver...")
                self.solve_captcha(driver)
            
            html = driver.page_source
            driver.quit()
            print("[+] Cloudflare bypass exitoso con Selenium")
            return html
        except Exception as e:
            print(f"[-] Error con Selenium: {e}")
        
        return None
    
    def solve_captcha(self, driver):
        """Intenta resolver captchas automáticamente"""
        try:
            # Buscar iframe de reCAPTCHA
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                if 'recaptcha' in iframe.get_attribute('src'):
                    driver.switch_to.frame(iframe)
                    # Click en el checkbox
                    checkbox = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")
                    checkbox.click()
                    time.sleep(2)
                    driver.switch_to.default_content()
                    print("[+] Captcha resuelto")
                    return True
        except:
            pass
        return False
    
    def bypass_akamai(self, url):
        """Bypass de Akamai"""
        # Akamai usa sensor de comportamiento
        session = requests.Session()
        
        # Simular comportamiento humano
        for _ in range(random.randint(3, 7)):
            session.get(url, timeout=10)
            time.sleep(random.uniform(0.5, 2))
        
        # Headers específicos
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Upgrade-Insecure-Requests': '1'
        })
        
        response = session.get(url)
        return response.text if response.status_code == 200 else None
    
    def rotate_ips(self):
        """Rota IPs usando proxies"""
        # Obtener proxies gratis
        proxy_sources = [
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
            'https://www.proxy-list.download/api/v1/get?type=http'
        ]
        
        for source in proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                proxies = response.text.split('\r\n')
                self.proxy_list = [p.strip() for p in proxies if p.strip()]
                break
            except:
                continue
        
        return self.proxy_list
    
    def auto_bypass(self, url):
        """Auto-detecta y bypass cualquier protección"""
        print(f"[🎯] Analizando protección de: {url}")
        
        # Detectar tipo de protección
        protection_type = self.detect_protection(url)
        
        if protection_type == 'cloudflare':
            return self.bypass_cloudflare(url)
        elif protection_type == 'akamai':
            return self.bypass_akamai(url)
        elif protection_type == 'ddos_guard':
            return self.bypass_ddos_guard(url)
        else:
            return self.standard_request(url)
    
    def detect_protection(self, url):
        """Detecta qué protección está activa"""
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            
            if 'cf-ray' in headers:
                return 'cloudflare'
            elif 'akamai' in str(headers).lower():
                return 'akamai'
            elif 'ddos-guard' in str(headers).lower():
                return 'ddos_guard'
            elif 'x-sucuri-id' in headers:
                return 'sucuri'
            else:
                return 'none'
        except:
            return 'unknown'
    
    def bypass_ddos_guard(self, url):
        """Bypass de DDoS-Guard"""
        session = requests.Session()
        
        # Simular navegación real
        session.get(url)
        time.sleep(1)
        
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-CL,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers'
        }
        
        session.headers.update(headers)
        response = session.get(url)
        
        # Verificar si hay JS challenge
        if 'Just a moment' in response.text or 'DDOS-GUARD' in response.text:
            print("[!] DDoS-Guard JS challenge detectado")
            # Aquí implementaríamos ejecución de JS
            return self.solve_js_challenge(url, session)
        
        return response.text if response.status_code == 200 else None
    
    def solve_js_challenge(self, url, session):
        """Resuelve challenges de JavaScript"""
        # Usar Selenium para ejecutar JS
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        time.sleep(10)  # Esperar que pase el challenge
        
        html = driver.page_source
        driver.quit()
        
        return html
    
    def standard_request(self, url):
        """Request estándar sin bypass"""
        try:
            response = requests.get(url, timeout=30)
            return response.text
        except:
            return None
