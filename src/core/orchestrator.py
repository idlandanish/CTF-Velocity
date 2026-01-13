"""
Component: Orchestrator
Role: Manages execution flow. Routes input -> Classifier -> Engine.
"""

from src.core.classifier import Classifier
from src.core.output_manager import OutputManager

# Import your engines
from src.engines.crypto_engine import CryptoEngine
from src.engines.web_engine import WebEngine
from src.engines.pwn_engine import PwnEngine
from src.engines.forensics_engine import ForensicsEngine
from src.engines.rev_engine import RevEngine

class Orchestrator:
    def __init__(self):
        self.out = OutputManager()
        self.classifier = Classifier()
        
        # Map classifier output strings to actual Engine Classes
        self.engine_map = {
            'crypto': CryptoEngine,
            'web': WebEngine,
            'pwn': PwnEngine,
            'forensics': ForensicsEngine,
            'rev': RevEngine,
            'misc': None 
        }

    def run(self, target):
        self.out.banner()
        self.out.info(f"Orchestrating analysis for: {target}")
        
        # 1. Identify the threat
        category = self.classifier.identify(target)
        
        # Colorize the classification result
        self.out.highlight("Classification Result", category.upper())
        
        # 2. Select the correct engine
        engine_class = self.engine_map.get(category)
        
        if not engine_class:
            self.out.warning(f"No automated engine available for '{category}' yet.")
            return

        # 3. Instantiate and Execute
        try:
            # Note: Ideally, engines would also accept 'self.out' to print colors,
            # but for now we just run them as-is.
            engine = engine_class()
            self.out.info(f"Handing over to {category.capitalize()} Engine...")
            engine.execute(target)
        except Exception as e:
            self.out.error(f"Engine Failure: {e}")