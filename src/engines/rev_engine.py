"""
Engine: Rev
Role: Automated workflow for Reverse Engineering (Hashing, Packing, Strings).
"""
import os
import hashlib
import re

class RevEngine:
    def execute(self, target):
        print(f"[*] [Rev] Starting Static Analysis on: {target}")
        
        if not os.path.exists(target):
            print(f"[-] Error: File not found: {target}")
            return

        self._basic_info(target)
        self._check_upx(target)
        self._extract_strings(target)

    def _basic_info(self, path):
        """Calculates file hash and size."""
        try:
            with open(path, 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
            print(f"    File Size: {len(data)} bytes")
            print(f"    MD5 Hash:  {md5}")
        except Exception as e:
            print(f"[-] Error reading file info: {e}")

    def _check_upx(self, path):
        """Checks for UPX packing signatures."""
        try:
            with open(path, 'rb') as f:
                content = f.read()
            
            # UPX usually leaves 'UPX!' markers in the binary
            if b'UPX!' in content:
                print("\n[!] PACKED DETECTED: UPX marker found!")
                print("    -> Recommendation: Run 'upx -d <file>' to unpack.")
            else:
                print("[*] No standard UPX packing markers detected.")
        except Exception:
            pass

    def _extract_strings(self, path):
        """Basic strings extraction to look for flags."""
        print("[*] Scanning for interesting strings...")
        found_something = False
        
        try:
            with open(path, 'rb') as f:
                content = f.read()
            
            # Find ASCII strings length 4+
            matches = re.findall(b"[ -~]{4,}", content)
            
            for match in matches:
                s = match.decode('utf-8', errors='ignore')
                # Simple heuristic for flags or interesting files
                if "flag" in s.lower() or "ctf" in s.lower() or "{" in s:
                    print(f"    >> Found String: {s}")
                    found_something = True
            
            if not found_something:
                print("    [-] No obvious flag strings found.")
                
        except Exception as e:
            print(f"[-] Strings error: {e}")