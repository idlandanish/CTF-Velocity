"""
Engine: Web
Role: Automated workflow for web challenges (Robots, Headers, Comments).
"""
import requests
from src.utils.flag_extractor import FlagExtractor

class WebEngine:
    def __init__(self):
        self.extractor = FlagExtractor()

    def execute(self, target):
        print(f"[*] [Web] Starting scan on: {target}")
        
        # Ensure URL has schema
        if not target.startswith("http"):
            target = "http://" + target

        self._check_robots(target)
        self._check_headers(target)

    def _check_robots(self, url):
        """Checks robots.txt for hidden paths."""
        robots_url = f"{url.rstrip('/')}/robots.txt"
        print(f"[*] Checking {robots_url}...")
        
        try:
            r = requests.get(robots_url, timeout=5)
            if r.status_code == 200:
                print(f"[+] Found robots.txt! Content preview:\n{r.text[:200]}\n")
                
                # Check for flags in the file itself
                flag = self.extractor.check(r.text)
                if flag:
                    print(f"[+] !!! FLAG FOUND IN ROBOTS.TXT: {flag} !!!")
            else:
                print("[-] No robots.txt found.")
        except Exception as e:
            print(f"[!] Error fetching robots.txt: {e}")

    def _check_headers(self, url):
        """Inspects HTTP headers for hidden info."""
        print(f"[*] Inspecting HTTP Headers...")
        try:
            r = requests.head(url, timeout=5)
            for key, value in r.headers.items():
                # CTFs often hide clues in custom headers (X-Flag, X-Secret)
                if "flag" in key.lower() or "ctf" in key.lower() or self.extractor.check(value):
                    print(f"[+] INTERESTING HEADER: {key}: {value}")
        except Exception as e:
            print(f"[!] Error fetching headers: {e}")
