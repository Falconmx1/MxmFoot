#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import json
import time
from datetime import datetime
from modules.dns_enum import DNSEnumerator
from modules.whois_lookup import WhoisLookup
from modules.web_scraper import WebScraper
from modules.social_finder import SocialFinder

class MXMFOOT:
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.modules = {
            'dns': DNSEnumerator(),
            'whois': WhoisLookup(),
            'web': WebScraper(),
            'social': SocialFinder()
        }
    
    def print_banner(self):
        try:
            with open('banners/banner.txt', 'r', encoding='utf-8') as f:
                print(f.read())
        except:
            print("""
    ███╗   ███╗██╗  ██╗███╗   ███╗
    ████╗ ████║╚██╗██╔╝████╗ ████║
    ██╔████╔██║ ╚███╔╝ ██╔████╔██║
    ██║╚██╔╝██║ ██╔██╗ ██║╚██╔╝██║
    ██║ ╚═╝ ██║██╔╝ ██╗██║ ╚═╝ ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
            """)
        print("[+] MXMFOOT - OSINT Weaponized")
        print(f"[+] Target: {self.target}")
        print("[+] Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60)
    
    def run_module(self, module_name):
        print(f"\n[*] Ejecutando módulo: {module_name.upper()}")
        try:
            if module_name in self.modules:
                result = self.modules[module_name].scan(self.target)
                self.results[module_name] = result
                print(f"[+] {module_name.upper()} completado")
            else:
                print(f"[-] Módulo {module_name} no existe")
        except Exception as e:
            print(f"[!] Error en {module_name}: {str(e)}")
    
    def run_all(self):
        for module in self.modules.keys():
            self.run_module(module)
            time.sleep(1)  # Pequeño delay para no ser bloqueado
    
    def save_results(self):
        filename = f"report_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"\n[+] Reporte guardado: {filename}")
    
    def show_summary(self):
        print("\n" + "="*60)
        print("[+] RESUMEN DE HALLAZGOS")
        print("="*60)
        for module, data in self.results.items():
            print(f"\n[*] {module.upper()}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    if value:
                        print(f"    - {key}: {value}")

def main():
    parser = argparse.ArgumentParser(description='MXMFOOT - Herramienta OSINT más cabrona que SpiderFoot')
    parser.add_argument('-t', '--target', required=True, help='Dominio o IP objetivo')
    parser.add_argument('-m', '--module', choices=['dns', 'whois', 'web', 'social', 'all'], 
                        default='all', help='Módulo a ejecutar')
    parser.add_argument('-o', '--output', help='Guardar resultados en archivo')
    
    args = parser.parse_args()
    
    tool = MXMFOOT(args.target)
    tool.print_banner()
    
    if args.module == 'all':
        tool.run_all()
    else:
        tool.run_module(args.module)
    
    tool.show_summary()
    
    if args.output or True:  # Siempre guarda por defecto
        tool.save_results()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detectado. Saliendo...")
        sys.exit(0)
