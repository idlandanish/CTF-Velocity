"""
Component: Output Module
Role: Handles standardized, colored output for the CLI.
"""
from colorama import init, Fore, Style

class OutputManager:
    def __init__(self):
        # Initialize colorama (autoreset=True resets color after each print)
        init(autoreset=True)

    def success(self, message):
        """Prints a success message (Green)."""
        print(f"{Fore.GREEN}[+] {message}")

    def error(self, message):
        """Prints an error message (Red)."""
        print(f"{Fore.RED}[-] {message}")

    def warning(self, message):
        """Prints a warning message (Yellow)."""
        print(f"{Fore.YELLOW}[!] {message}")

    def info(self, message):
        """Prints an info message (Blue/White)."""
        print(f"{Fore.BLUE}[*]{Style.RESET_ALL} {message}")

    def highlight(self, key, value):
        """Prints a key-value pair with the key highlighted."""
        print(f"    {Fore.CYAN}{key}:{Style.RESET_ALL} {value}")

    def banner(self):
        """Prints the tool banner."""
        print(f"{Fore.MAGENTA}---------------------------------------")
        print(f"{Fore.MAGENTA}      CTF COPILOT - v1.0 Alpha         ")
        print(f"{Fore.MAGENTA}---------------------------------------{Style.RESET_ALL}")