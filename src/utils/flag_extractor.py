import re

class FlagExtractor:
    def __init__(self, patterns=None):
        if patterns is None:
            # Common flag formats
            self.patterns = [
                r"CTF\{.*?\}",       # CTF{...}
                r"flag\{.*?\}",      # flag{...}
                r"Cyber\{.*?\}",     # Cyber{...}
            ]
        else:
            self.patterns = patterns

    def check(self, text):
        """Returns the flag if found, otherwise None."""
        if not text or not isinstance(text, str):
            return None
            
        for pattern in self.patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None