"""
Engine: Crypto
Role: Automated workflow for basic encoding and cipher challenges.
"""
import base64
import binascii
import codecs
from src.utils.flag_extractor import FlagExtractor

class CryptoEngine:
    def __init__(self):
        self.extractor = FlagExtractor()

    def execute(self, target):
        print(f"[*] [Crypto] Attempting generic decodes on: {target[:30]}...")
        
        # List of decoding strategies to try
        strategies = [
            ("Base64", self._try_base64),
            ("Hex", self._try_hex),
            ("Reverse", self._try_reverse),
            ("ROT13", self._try_rot13)
        ]

        found_flag = False

        for name, method in strategies:
            try:
                result = method(target)
                if result:
                    # check if the result looks like a flag
                    flag = self.extractor.check(result)
                    if flag:
                        print(f"\n[+] SUCCESS! Strategy [{name}] found a flag:")
                        print(f"    >> {flag}")
                        found_flag = True
                    else:
                        # Even if no flag, print valid decoded text (it might be a hint)
                        # Only print if it looks like readable text (no weird bytes)
                        if result.isprintable() and len(result) > 4:
                            print(f"    - [{name}] Decoded: {result}")
            except Exception:
                pass # Strategy failed (e.g., input wasn't valid Base64), just skip

        if not found_flag:
            print("[-] No obvious flags found with basic decoders.")

    # --- Strategies ---

    def _try_base64(self, data):
        # Add padding if missing
        padding = len(data) % 4
        if padding:
            data += '=' * (4 - padding)
        return base64.b64decode(data).decode('utf-8', errors='ignore')

    def _try_hex(self, data):
        # Remove spaces or 0x prefixes
        clean = data.replace(" ", "").replace("0x", "")
        return bytes.fromhex(clean).decode('utf-8', errors='ignore')

    def _try_reverse(self, data):
        return data[::-1]

    def _try_rot13(self, data):
        return codecs.decode(data, 'rot_13')