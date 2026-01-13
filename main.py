#!/usr/bin/env python3
"""
CTF Copilot - Main Entry Point
"""
import sys
import os

# Ensure python can find our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.orchestrator import Orchestrator

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target_file_or_string>")
        return

    target = sys.argv[1]
    
    # Initialize and Run
    copilot = Orchestrator()
    copilot.run(target)

if __name__ == "__main__":
    main()