import random
from typing import List, Optional

class ProxyManager:
    def __init__(self, proxy_file: str = "proxies.txt"):
        self.proxy_file = proxy_file
        self.proxies: List[str] = []
        self.load_proxies()

    def load_proxies(self) -> None:
        """Load proxies from the proxy file."""
        try:
            with open(self.proxy_file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            if not self.proxies:
                raise ValueError("No proxies found in the proxy file")
        except FileNotFoundError:
            raise FileNotFoundError(f"Proxy file '{self.proxy_file}' not found")

    def get_random_proxy(self) -> Optional[str]:
        """Get a random proxy from the loaded proxies."""
        return random.choice(self.proxies) if self.proxies else None

    def get_proxy_count(self) -> int:
        """Get the total number of available proxies."""
        return len(self.proxies)

    def format_proxy_for_selenium(self, proxy: str) -> dict:
        """Format proxy string for Selenium WebDriver."""
        if not proxy:
            return {}
        
        return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        } 