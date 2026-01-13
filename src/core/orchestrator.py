"""
Component: Orchestrator
Role: Manages execution flow. Routes input -> Classifier -> Engine.
"""

from src.core.classifier import Classifier
# Import your engines (even if they are empty for now)
from src.engines.crypto_engine import CryptoEngine
from src.engines.web_engine import WebEngine
from src.engines.pwn_engine import PwnEngine
from src.engines.forensics_engine import ForensicsEngine
from src.engines.rev_engine import RevEngine

class Orchestrator:
    def __init__(self):
        self.classifier = Classifier()
        
        # Map classifier output strings to actual Engine Classes
        self.engine_map = {
            'crypto': CryptoEngine,
            'web': WebEngine,
            'pwn': PwnEngine,
            'forensics': ForensicsEngine,
            'rev': RevEngine,
            'misc': None # We will handle misc later
        }

    def run(self, target):
        print(f"[*] Orchestrating analysis for: {target}")
        
        # 1. Identify the threat
        category = self.classifier.identify(target)
        print(f"[*] Classification Result: {category.upper()}")
        
        # 2. Select the correct engine
        engine_class = self.engine_map.get(category)
        
        if not engine_class:
            print(f"[!] No automated engine available for '{category}' yet.")
            return

        # 3. Instantiate and Execute
        try:
            engine = engine_class()
            print(f"[*] Handing over to {category.capitalize()} Engine...")
            engine.execute(target)
        except Exception as e:
            print(f"[!] Engine Failure: {e}")