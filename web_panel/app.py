#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime

# Agregar módulos al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.shodan_intel import ShodanIntel
from modules.darkweb_scanner import DarkWebScanner
from modules.ai_recon import AIRecon
from modules.dns_enum import DNSEnumerator
from modules.whois_lookup import WhoisLookup

app = Flask(__name__)
CORS(app)

# Cargar config
with open('../config/api_keys.json', 'r') as f:
    config = json.load(f)

shodan = ShodanIntel(config.get('shodan_api_key'))
darkweb = DarkWebScanner()
ai = AIRecon()

# Store de resultados
scan_results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def start_scan():
    target = request.json.get('target')
    scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    results = {
        'target': target,
        'scan_id': scan_id,
        'timestamp': datetime.now().isoformat(),
        'modules': {}
    }
    
    # DNS Enum
    dns = DNSEnumerator()
    results['modules']['dns'] = dns.scan(target)
    
    # Whois
    whois = WhoisLookup()
    results['modules']['whois'] = whois.scan(target)
    
    # Shodan
    results['modules']['shodan'] = shodan.search_domain(target)
    
    # Dark Web
    darkweb.setup_tor()
    results['modules']['darkweb'] = darkweb.search_onion(target)
    results['modules']['leaked_data'] = darkweb.check_leaked_data(target)
    
    # AI
    results['modules']['ai'] = ai.smart_enumeration(target)
    
    scan_results[scan_id] = results
    
    return jsonify({'scan_id': scan_id, 'status': 'completed'})

@app.route('/api/results/<scan_id>')
def get_results(scan_id):
    if scan_id in scan_results:
        return jsonify(scan_results[scan_id])
    return jsonify({'error': 'Scan not found'}), 404

@app.route('/api/graph/<scan_id>')
def graph_data(scan_id):
    """Datos para visualización tipo BloodHound"""
    if scan_id not in scan_results:
        return jsonify({'error': 'Not found'}), 404
    
    results = scan_results[scan_id]
    
    # Construir graph data para D3.js
    nodes = []
    edges = []
    
    # Nodo principal
    nodes.append({'id': results['target'], 'group': 'target', 'size': 30})
    
    # Subdominios
    if 'dns' in results['modules']:
        for sub in results['modules']['dns'].get('subdomains', [])[:10]:
            nodes.append({'id': sub, 'group': 'subdomain', 'size': 15})
            edges.append({'source': results['target'], 'target': sub})
    
    # IPs/Ports de Shodan
    if 'shodan' in results['modules'] and 'open_ports' in results['modules']['shodan']:
        for port in results['modules']['shodan'].get('open_ports', [])[:5]:
            port_id = f"port_{port.get('port')}"
            nodes.append({'id': port_id, 'group': 'port', 'size': 10})
            edges.append({'source': results['target'], 'target': port_id})
    
    # Vulnerabilidades
    if 'ai' in results['modules']:
        for vuln in results['modules']['ai'].get('potential_vulnerabilities', []):
            vuln_id = vuln.get('type')[:20]
            nodes.append({'id': vuln_id, 'group': 'vuln', 'size': 20})
            edges.append({'source': results['target'], 'target': vuln_id})
    
    return jsonify({'nodes': nodes, 'edges': edges})

@app.route('/api/export/<scan_id>')
def export_report(scan_id):
    if scan_id in scan_results:
        return jsonify(scan_results[scan_id])
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
