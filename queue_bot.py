import os
import time
from typing import Optional
from session_manager import SessionManager
from notifier import Notifier
from dotenv import load_dotenv

def load_config() -> dict:
    """Load configuration from environment variables."""
    load_dotenv()
    
    return {
        'target_url': os.getenv('TARGET_URL', 'https://www.pokemoncenter.com/en-ca/product/10-10037-118'),
        'queue_threshold': int(os.getenv('QUEUE_THRESHOLD', '1000')),
        'headless': os.getenv('HEADLESS', 'true').lower() == 'true',
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'email': os.getenv('EMAIL'),
        'email_password': os.getenv('EMAIL_PASSWORD')
    }

def main():
    """Main function to run the queue bot."""
    try:
        # Load configuration
        config = load_config()
        
        # Initialize notifier
        if not config['email'] or not config['email_password']:
            print("Email credentials not provided. Please set EMAIL and EMAIL_PASSWORD in .env file")
            return

        notifier = Notifier(
            smtp_server=config['smtp_server'],
            smtp_port=config['smtp_port'],
            email=config['email'],
            password=config['email_password']
        )
        
        # Initialize session manager
        session_manager = SessionManager(
            target_url=config['target_url'],
            queue_threshold=config['queue_threshold'],
            headless=config['headless'],
            notifier=notifier
        )

        print(f"Starting queue bot for {config['target_url']}")
        print(f"Queue threshold: {config['queue_threshold']}")
        print(f"Email notifications enabled for: {config['email']}")

        # Start monitoring the queue
        session_manager.monitor_queue()

    except KeyboardInterrupt:
        print("\nQueue bot stopped by user")
    except Exception as e:
        print(f"Error running queue bot: {e}")
    finally:
        if 'session_manager' in locals():
            session_manager.cleanup()

if __name__ == "__main__":
    main() 