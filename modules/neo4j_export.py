#!/usr/bin/env python3
from neo4j import GraphDatabase
import json
from datetime import datetime
from colorama import Fore

class Neo4jExport:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.connect()
    
    def connect(self):
        """Conecta a Neo4j"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            print(f"{Fore.GREEN}[+] Conectado a Neo4j en {self.uri}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Error conectando a Neo4j: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Instala Neo4j con: docker run -p 7474:7474 -p 7687:7687 neo4j{Style.RESET_ALL}")
            return False
    
    def create_constraints(self):
        """Crea constraints para optimización"""
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Target) REQUIRE n.name IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:IP) REQUIRE n.address IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Domain) REQUIRE n.name IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Vulnerability) REQUIRE n.cve IS UNIQUE")
    
    def export_target(self, target_data):
        """Exporta target principal"""
        with self.driver.session() as session:
            # Crear nodo target
            session.run("""
                MERGE (t:Target {name: $name})
                SET t.first_seen = $timestamp,
                    t.risk_score = $risk_score,
                    t.technologies = $technologies
            """, name=target_data['target'], 
                timestamp=target_data['timestamp'],
                risk_score=target_data.get('risk_score', 0),
                technologies=target_data.get('technologies', []))
            
            return True
    
    def export_dns_relations(self, target, dns_data):
        """Exporta relaciones DNS"""
        with self.driver.session() as session:
            for subdomain in dns_data.get('subdomains', []):
                session.run("""
                    MERGE (s:Subdomain {name: $subdomain})
                    MERGE (t:Target {name: $target})
                    MERGE (s)-[:BELONGS_TO]->(t)
                    SET s.detected = $timestamp
                """, subdomain=subdomain, target=target, timestamp=datetime.now().isoformat())
            
            # Relaciones MX
            for mx in dns_data.get('MX', []):
                session.run("""
                    MERGE (m:MailServer {address: $mx})
                    MERGE (t:Target {name: $target})
                    MERGE (t)-[:USES_MAIL_SERVER]->(m)
                """, mx=mx, target=target)
    
    def export_vulnerabilities(self, target, vuln_data):
        """Exporta vulnerabilidades encontradas"""
        with self.driver.session() as session:
            for vuln in vuln_data:
                cve = vuln.get('cve', vuln.get('type', 'Unknown'))
                session.run("""
                    MERGE (v:Vulnerability {cve: $cve})
                    SET v.severity = $severity,
                        v.description = $description,
                        v.exploit_exists = $exploit_exists
                    MERGE (t:Target {name: $target})
                    MERGE (t)-[:AFFECTED_BY]->(v)
                """, cve=cve, 
                    severity=vuln.get('severity', 'MEDIUM'),
                    description=vuln.get('description', ''),
                    exploit_exists=vuln.get('exploit_exists', False),
                    target=target)
    
    def export_social_graph(self, target, social_data):
        """Exporta relaciones sociales (Telegram/Discord)"""
        with self.driver.session() as session:
            # Telegram
            for channel in social_data.get('telegram', {}).get('channels', []):
                session.run("""
                    MERGE (tg:TelegramChannel {name: $name})
                    SET tg.url = $url, tg.members = $members
                    MERGE (t:Target {name: $target})
                    MERGE (t)-[:HAS_TELEGRAM]->(tg)
                """, name=channel['name'], url=channel['url'], 
                    members=channel.get('members', 0), target=target)
            
            # Discord
            for server in social_data.get('discord', {}).get('servers', []):
                session.run("""
                    MERGE (ds:DiscordServer {name: $name})
                    SET ds.id = $id, ds.members = $members
                    MERGE (t:Target {name: $target})
                    MERGE (t)-[:HAS_DISCORD]->(ds)
                """, name=server['name'], id=server['id'],
                    members=server.get('members', 0), target=target)
    
    def export_leaks(self, target, leak_data):
        """Exporta leaks encontrados en GitHub"""
        with self.driver.session() as session:
            for leak_type, leaks in leak_data.get('leaks', {}).items():
                for leak in leaks[:10]:  # Limit to 10 per type
                    session.run("""
                        MERGE (l:Leak {file: $file})
                        SET l.type = $type, l.repo = $repo
                        MERGE (t:Target {name: $target})
                        MERGE (t)-[:LEAKED_ON]->(l)
                    """, file=leak['file'], type=leak_type,
                        repo=leak['repo'], target=target)
    
    def execute_bloodhound_query(self, target):
        """Ejecuta queries tipo BloodHound"""
        with self.driver.session() as session:
            # Query para encontrar caminos de ataque
            result = session.run("""
                MATCH (t:Target {name: $target})
                MATCH (v:Vulnerability)
                WHERE (t)-[:AFFECTED_BY]->(v)
                RETURN t.name as Target, 
                       collect(v.cve) as Vulnerabilities,
                       count(v) as VulnCount
                ORDER BY VulnCount DESC
            """, target=target)
            
            return [dict(record) for record in result]
    
    def close(self):
        """Cierra conexión"""
        if self.driver:
            self.driver.close()
