#!/usr/bin/env python3
import requests
import json
import re
import asyncio
from datetime import datetime
from colorama import Fore, Style

class SocialRecon:
    def __init__(self, telegram_bot_token=None, discord_bot_token=None):
        self.telegram_token = telegram_bot_token
        self.discord_token = discord_bot_token
        self.session = requests.Session()
        
    def telegram_search(self, query):
        """Busca información en Telegram"""
        print(f"{Fore.BLUE}[*] Buscando en Telegram: {query}{Style.RESET_ALL}")
        
        results = {
            'channels': [],
            'groups': [],
            'users': [],
            'messages': []
        }
        
        # Método 1: Usar API pública de Telegram (limitada)
        if self.telegram_token:
            try:
                # Buscar usuarios
                url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    for update in data.get('result', []):
                        if 'message' in update:
                            text = update['message'].get('text', '')
                            if query.lower() in text.lower():
                                results['messages'].append({
                                    'chat_id': update['message']['chat']['id'],
                                    'text': text[:200],
                                    'date': datetime.fromtimestamp(update['message']['date']).isoformat()
                                })
            except:
                pass
        
        # Método 2: Scraping de grupos públicos (simulado para demo)
        # En la vida real usaríamos telethon o pyrogram
        
        # Simulación de resultados (para demostración)
        simulated = {
            'channels': [
                {'name': f'{query}_official', 'members': 15432, 'url': f't.me/{query}_official'},
                {'name': f'{query}_community', 'members': 8921, 'url': f't.me/{query}_community'}
            ],
            'groups': [
                {'name': f'{query} Hackers', 'members': 2341, 'url': f't.me/+abc123'},
                {'name': f'{query} Security', 'members': 5678, 'url': f't.me/+def456'}
            ],
            'users': [
                {'username': f'{query}_admin', 'first_name': f'{query} Admin', 'id': 123456789},
                {'username': f'@{query}sec', 'first_name': 'Security Expert', 'id': 987654321}
            ]
        }
        
        results.update(simulated)
        return results
    
    def discord_search(self, query):
        """Busca información en Discord"""
        print(f"{Fore.BLUE}[*] Buscando en Discord: {query}{Style.RESET_ALL}")
        
        results = {
            'servers': [],
            'channels': [],
            'messages': [],
            'invites': []
        }
        
        # Método 1: Usar Discord API (requiere bot)
        if self.discord_token:
            try:
                headers = {'Authorization': f'Bot {self.discord_token}'}
                
                # Buscar servidores (solo los que el bot está)
                url = "https://discord.com/api/v10/users/@me/guilds"
                response = self.session.get(url, headers=headers)
                
                if response.status_code == 200:
                    guilds = response.json()
                    for guild in guilds:
                        if query.lower() in guild['name'].lower():
                            results['servers'].append({
                                'name': guild['name'],
                                'id': guild['id'],
                                'members': guild.get('approximate_member_count', 'N/A')
                            })
            except:
                pass
        
        # Método 2: Scraping de invites públicos (disboard, top.gg)
        try:
            # Buscar en Disboard
            disboard_url = f"https://disboard.org/servers/tag/{query}"
            response = self.session.get(disboard_url)
            
            # Extraer invites (simplificado)
            invites = re.findall(r'discord\.gg/([a-zA-Z0-9]+)', response.text)
            for invite in invites[:10]:
                results['invites'].append({
                    'code': invite,
                    'url': f'discord.gg/{invite}'
                })
        except:
            pass
        
        # Datos simulados para demo
        simulated = {
            'servers': [
                {'name': f'{query} Official', 'members': 15000, 'id': '123456789'},
                {'name': f'{query} Community', 'members': 2500, 'id': '987654321'}
            ],
            'invites': [
                {'code': f'{query}123', 'url': f'discord.gg/{query}123'},
                {'code': f'{query}discord', 'url': f'discord.gg/{query}discord'}
            ]
        }
        
        results.update(simulated)
        return results
    
    def extract_sensitive_info(self, text):
        """Extrae info sensible de mensajes"""
        patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\+\d{1,3}\s?\d{3}\s?\d{3}\s?\d{4}',
            'ip': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'url': r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
            'crypto': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}'
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                extracted[key] = matches[:5]
        
        return extracted
    
    def search_all_platforms(self, query):
        """Busca en todas las plataformas sociales"""
        results = {
            'telegram': self.telegram_search(query),
            'discord': self.discord_search(query),
            'timestamp': datetime.now().isoformat()
        }
        
        # Extraer info sensible
        for platform, data in results.items():
            if platform != 'timestamp':
                for category in data:
                    if isinstance(data[category], list):
                        for item in data[category]:
                            if 'text' in item or 'description' in item:
                                text = str(item.get('text', '')) + str(item.get('description', ''))
                                item['sensitive_data'] = self.extract_sensitive_info(text)
        
        return results
