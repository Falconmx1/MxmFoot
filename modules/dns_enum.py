import dns.resolver
import socket

class DNSEnumerator:
    def scan(self, domain):
        results = {
            'A': [],
            'MX': [],
            'NS': [],
            'TXT': [],
            'subdomains': []
        }
        
        # Enumeración básica de DNS
        record_types = ['A', 'MX', 'NS', 'TXT']
        for record in record_types:
            try:
                answers = dns.resolver.resolve(domain, record)
                for rdata in answers:
                    results[record].append(str(rdata))
            except:
                pass
        
        # Subdominios comunes
        common_subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test', 'api']
        for sub in common_subs:
            try:
                target = f"{sub}.{domain}"
                ip = socket.gethostbyname(target)
                results['subdomains'].append(f"{target} -> {ip}")
            except:
                pass
        
        return results
