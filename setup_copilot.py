import os
import sys

def create_file(path, content=""):
    """Helper to create a file with content."""
    with open(path, 'w') as f:
        f.write(content)
    print(f"[+] Created: {path}")

def main():
    base_dir = "CTF_Copilot"
    print(f"[*] Initializing {base_dir} Project Structure based on PDI...")

    # 1. Define the directory tree
    dirs = [
        f"{base_dir}/src",
        f"{base_dir}/src/core",         # Orchestrator, Classifier, Input Handler
        f"{base_dir}/src/engines",      # Category specific logic (Crypto, Web, etc.)
        f"{base_dir}/src/wrappers",     # External tool wrappers (Safe interfaces)
        f"{base_dir}/src/interface",    # CLI handling
        f"{base_dir}/src/utils",        # Logging, config, formatting
        f"{base_dir}/tests",            # Test cases (Phase 4 of Timeline)
        f"{base_dir}/logs",             # Log storage
        f"{base_dir}/docs",             # Documentation
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 2. Create Core Components (PDI Section 8)
    
    # Input Handler
    create_file(f"{base_dir}/src/core/input_handler.py", 
'''"""
Component: Input Handler
Role: Accepts files, URLs, or text and prepares them for the Orchestrator.
"""

class InputHandler:
    def parse(self, user_input):
        # TODO: Implement file/URL detection
        pass
''')

    # Category Classifier
    create_file(f"{base_dir}/src/core/classifier.py", 
'''"""
Component: Category Classifier
Role: Identifies challenge type (Crypto, Web, Pwn) based on input signatures.
"""

class Classifier:
    def identify(self, data):
        # TODO: Implement magic byte or pattern analysis
        return "UNKNOWN"
''')

    # Orchestrator
    create_file(f"{base_dir}/src/core/orchestrator.py", 
'''"""
Component: Orchestrator
Role: Manages execution flow. Routes input -> Classifier -> Engine.
"""

class Orchestrator:
    def run(self, target):
        print(f"[*] Orchestrating analysis for: {target}")
        # Flow: 
        # 1. Classifier.identify(target)
        # 2. Engines.get_engine(type).execute()
        pass
''')

    # Output Module
    create_file(f"{base_dir}/src/core/output_manager.py", 
'''"""
Component: Output Module
Role: Extracts flags and generates logs.
"""
''')

    # 3. Create Category Engines (PDI Section 8 & 5)
    engines = ["crypto", "web", "pwn", "rev", "forensics"]
    create_file(f"{base_dir}/src/engines/__init__.py", "")
    for engine in engines:
        create_file(f"{base_dir}/src/engines/{engine}_engine.py", 
f'''"""
Engine: {engine.capitalize()}
Role: Automated workflow for {engine} challenges.
"""

class {engine.capitalize()}Engine:
    def execute(self, target):
        print(f"[*] Running {engine} workflows on {{target}}...")
''')

    # 4. Create Tool Wrappers (PDI Section 8 - "Structured Wrappers")
    create_file(f"{base_dir}/src/wrappers/__init__.py", "")
    create_file(f"{base_dir}/src/wrappers/tool_runner.py", 
'''"""
Base class for safe external tool execution.
"""
import subprocess

class ToolRunner:
    def run_command(self, cmd):
        # TODO: Implement safe subprocess execution with timeout
        pass
''')

    # 5. Main Entry Point (CLI)
    create_file(f"{base_dir}/main.py", 
'''#!/usr/bin/env python3
"""
CTF Copilot - Main Entry Point
"""
import sys
from src.core.orchestrator import Orchestrator

def main():
    print("---------------------------------------")
    print("      CTF COPILOT - v1.0 Alpha         ")
    print("---------------------------------------")
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <target_file_or_string>")
        return

    target = sys.argv[1]
    copilot = Orchestrator()
    copilot.run(target)

if __name__ == "__main__":
    main()
''')

    # 6. Documentation & Requirements
    create_file(f"{base_dir}/requirements.txt", 
'''pwntools
requests
pycryptodome
python-magic
colorama
''')
    
    create_file(f"{base_dir}/README.md", 
'''# CTF Copilot

## Project Definition
An automated assistance framework for Capture The Flag (CTF) challenges.

## Architecture
1. **Input Handler**: Ingests data.
2. **Classifier**: Determines category (Crypto/Web/etc).
3. **Engines**: Runs specific workflows.
4. **Wrappers**: Interfaces with tools like SQLMap or Volatility.

## Usage
`python main.py <target>`
''')

    print("\n[✔] Project Created Successfully.")
    print(f"    Location: ./{base_dir}")
    print("    Next Step: 'cd CTF_Copilot' and open in VS Code.")

if __name__ == "__main__":
    main()