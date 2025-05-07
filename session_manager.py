import time
import json
from typing import Optional
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from proxy_manager import ProxyManager
from notifier import Notifier

class SessionManager:
    def __init__(self, target_url: str, queue_threshold: int = 100, headless: bool = True, notifier: Optional[Notifier] = None):
        self.target_url = target_url
        self.queue_threshold = queue_threshold
        self.headless = headless
        self.proxy_manager = ProxyManager()
        self.driver: Optional[webdriver.Chrome] = None
        self.notifier = notifier
        self.last_notified_position = None

    def create_driver(self, proxy: str) -> Optional[webdriver.Chrome]:
        """Create a new Chrome WebDriver instance with the specified proxy."""
        try:
            print(f"Attempting to create driver with proxy: {proxy}")
            
            chrome_options = uc.ChromeOptions()
            if self.headless:
                chrome_options.add_argument('--headless=new')  # Using new headless mode
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Add proxy settings
            if proxy:
                chrome_options.add_argument(f'--proxy-server={proxy}')
                print(f"Added proxy: {proxy}")

            driver = uc.Chrome(options=chrome_options)
            print("Successfully created Chrome driver")
            return driver
        except Exception as e:
            print(f"Error creating driver with proxy {proxy}: {e}")
            return None

    def notify_queue_position(self, position: int) -> None:
        """Send email notification if queue position has changed significantly."""
        if self.notifier and (self.last_notified_position is None or 
                            abs(position - self.last_notified_position) >= 1000):
            self.notifier.notify_queue_position(
                position=position,
                threshold=self.queue_threshold,
                recipient=self.notifier.email  # Send to self
            )
            self.last_notified_position = position

    def get_queue_position(self) -> Optional[int]:
        """Get the current queue position from the Incapsula JSON response."""
        try:
            response = self.driver.execute_script("""
                return new Promise((resolve, reject) => {
                    fetch('https://www.pokemoncenter.com/_Incapsula_Resource?SWWRGTS=868', {
                        method: 'GET',
                        headers: {
                            'Accept': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => resolve(data ? data.pos : null))
                    .catch(error => {
                        console.error('Fetch error:', error);
                        resolve(null);
                    });
                });
            """)
            position = int(response) if response else None
            if position:
                self.notify_queue_position(position)
            return position
        except Exception as e:
            print(f"Error getting queue position: {e}")
            return None

    def monitor_queue(self) -> None:
        """Monitor the queue position and send notifications."""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                proxy = self.proxy_manager.get_random_proxy()
                if not proxy:
                    raise ValueError("No proxies available")

                print(f"Attempting to create driver with proxy {proxy} (attempt {retry_count + 1}/{max_retries})")
                self.driver = self.create_driver(proxy)
                if not self.driver:
                    retry_count += 1
                    print(f"Failed to create driver, retrying... ({retry_count}/{max_retries})")
                    time.sleep(5)
                    continue

                print(f"Navigating to {self.target_url}")
                self.driver.get(self.target_url)

                while True:
                    position = self.get_queue_position()
                    if position is None:
                        print("Failed to get queue position, retrying...")
                        time.sleep(5)
                        continue

                    print(f"Current queue position: {position}")
                    
                    if position <= self.queue_threshold:
                        print(f"Queue position {position} is below threshold {self.queue_threshold}")
                        if self.notifier:
                            self.notifier.notify_queue_position(
                                position=position,
                                threshold=self.queue_threshold,
                                recipient=self.notifier.email,
                                subject="URGENT: Queue Position Below Threshold!"
                            )
                        break

                    time.sleep(5)  # Wait before checking again
                break  # Successfully completed monitoring

            except Exception as e:
                print(f"Error in queue monitoring: {e}")
                if self.driver:
                    self.driver.quit()
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Retrying with a different proxy... ({retry_count}/{max_retries})")
                    time.sleep(5)
                else:
                    print("Max retries reached. Exiting.")
                    break

    def cleanup(self) -> None:
        """Clean up resources."""
        if self.driver:
            self.driver.quit() 