"""
Engine: Forensics
Role: Automated workflow for file analysis (Strings, Metadata).
"""
import os
import re
from src.utils.flag_extractor import FlagExtractor

class ForensicsEngine:
    def __init__(self):
        self.extractor = FlagExtractor()

    def execute(self, filepath):
        print(f"[*] [Forensics] Starting analysis on file: {filepath}")
        
        if not os.path.exists(filepath):
            print(f"[-] Error: File not found: {filepath}")
            return

        # Strategy 1: The "Strings" Method (Read file, look for readable text)
        print("[*] Running 'strings' extraction...")
        found_flags = self._analyze_strings(filepath)
        
        if found_flags:
            print("\n[+] SUCCESS! Found potential flags in file binary:")
            for flag in found_flags:
                print(f"    >> {flag}")
        else:
            print("[-] No obvious flags found in plaintext strings.")

    def _analyze_strings(self, filepath, min_length=4):
        """
        Equivalent to the Linux 'strings' command. 
        Reads binary file and extracts sequences of printable characters.
        """
        found = set()
        
        try:
            with open(filepath, "rb") as f:
                content = f.read()
                
            # Regex to find sequences of 4+ printable characters
            # ASCII range 32-126 (standard printable)
            # This regex looks for bytes that act like text
            matches = re.findall(b"[ -~]{4,}", content)
            
            for match in matches:
                text_str = match.decode('utf-8', errors='ignore')
                
                # Check this string against our Flag Extractor
                flag = self.extractor.check(text_str)
                if flag:
                    found.add(flag)
                    
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            
        return list(found)