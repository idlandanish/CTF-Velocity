"""
Engine: Pwn
Role: Automated workflow for pwn challenges (Checksec, vulnerability scanning).
"""
import os
import sys

# Attempt to import pwntools, handle missing dependency gracefully
try:
    from pwn import ELF, context
    PWNTOOLS_AVAILABLE = True
except ImportError:
    PWNTOOLS_AVAILABLE = False

class PwnEngine:
    def execute(self, target):
        print(f"[*] [Pwn] Starting analysis on: {target}")
        
        if not os.path.exists(target):
            print(f"[-] Error: File not found: {target}")
            return

        if not PWNTOOLS_AVAILABLE:
            print("[-] Error: 'pwntools' library not installed. Cannot run checksec.")
            print("    Please run: pip install pwntools")
            return

        self._run_checksec(target)

    def _run_checksec(self, filepath):
        """
        Uses pwntools to check for binary protections (NX, PIE, Canary, RELRO).
        """
        print(f"[*] Running Checksec on {os.path.basename(filepath)}...")
        
        try:
            # Load the binary with pwntools
            # context.log_level = 'error' # Suppress pwntools noisy banner
            binary = ELF(filepath, checksec=False)
            
            print("\n    [ Security Protections ]")
            print(f"    Arch:    {binary.arch}-{binary.bits}-{binary.endian}")
            print(f"    RELRO:   {self._color_status(binary.relro)}")
            print(f"    Canary:  {self._color_status(binary.canary)}")
            print(f"    NX:      {self._color_status(binary.nx)}")
            print(f"    PIE:     {self._color_status(binary.pie)}")
            print("")

        except Exception as e:
            print(f"[-] Failed to load binary: {e}")

    def _color_status(self, status):
        """Helper to format status strings."""
        # Simple text formatting since we might not have colorama
        if status is True or status == 'Full':
             return "ENABLED  (Secure)"
        elif status is False or status == 'No':
             return "DISABLED (Vulnerable)"
        return str(status)
