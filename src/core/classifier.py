"""
Component: Category Classifier
Role: Identifies challenge type (Crypto, Web, Pwn, Forensics) based on input signatures.
"""

import os
import re
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

class Classifier:
    def __init__(self):
        # Mappings of MIME types to CTF Categories
        self.mime_map = {
            'application/x-executable': 'pwn',      # Linux ELF
            'application/x-pie-executable': 'pwn',  # Linux ELF (PIE)
            'application/x-dosexec': 'pwn',         # Windows PE
            'application/x-sharedlib': 'rev',       # Shared libraries
            'text/x-python': 'rev',                 # Source code
            'text/x-c': 'rev',
            'image/jpeg': 'forensics',
            'image/png': 'forensics',
            'application/zip': 'forensics',         # Archives usually hide stuff
            'application/x-tar': 'forensics',
            'application/vnd.tcpdump.pcap': 'forensics' # Wireshark captures
        }

    def identify(self, target):
        """
        Analyzes the target (file path or string) and returns the Category.
        """
        # 1. Check if it is a valid file path
        if os.path.exists(target):
            return self._analyze_file(target)
        
        # 2. Treat as string/text input
        return self._analyze_text(target)

    def _analyze_file(self, filepath):
        """Uses Magic Bytes to detect file type."""
        
        # PRIORITY 1: Check Extension for Source Code (Overrides magic for scripts)
        # Magic often mistakes small .py files for generic text/plain
        if filepath.lower().endswith('.py'):
            return 'rev'
        if filepath.lower().endswith('.c') or filepath.lower().endswith('.cpp'):
            return 'rev'

        # PRIORITY 2: Magic Bytes
        if not MAGIC_AVAILABLE:
            return 'misc'

        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(filepath)
            print(f"[+] Detected File Type: {file_type}")

            # SMART CHECK: If generic binary, check specific magic bytes manually
            if file_type == 'application/octet-stream':
                try:
                    with open(filepath, 'rb') as f:
                        header = f.read(4)
                    if header.startswith(b'\x7fELF') or header.startswith(b'MZ'):
                        return 'pwn'
                except Exception:
                    pass

            # Match against our standard map
            category = self.mime_map.get(file_type, 'misc')
            
            # Special check: If it's a text file, it might be a key or source
            if 'text' in file_type and category == 'misc':
                return 'crypto' 
            
            return category

        except Exception as e:
            print(f"[!] Classification Error: {e}")
            return 'misc'

    def _analyze_text(self, text):
        """Uses Regex patterns to detect Strings, URLs, hashes."""
        if text.startswith('http://') or text.startswith('https://'):
            return 'web'
        
        if re.match(r'^[A-Za-z0-9+/]+={0,2}$', text) and len(text) > 8:
            return 'crypto'
        
        if re.match(r'^[a-fA-F0-9]+$', text) and len(text) > 8:
            return 'crypto'
            
        return 'misc'
