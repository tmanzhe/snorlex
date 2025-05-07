# Queue Bot with Proxy IPs

A Python-based queue bot that automatically monitors queue positions using multiple proxy IPs. When a session's queue position drops below a specified threshold, it automatically opens the session for manual checkout.

## Features

- Multiple proxy IP support
- Automatic queue position monitoring
- Browser automation with Selenium
- Optional email notifications
- Configurable queue threshold
- Headless/headed mode support

## Requirements

- Python 3.7+
- Chrome browser
- Proxy IPs (one per line in proxies.txt)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `proxies.txt` file with your proxy IPs (one per line, format: IP:PORT)
4. Copy `.env.example` to `.env` and configure your settings

## Configuration

Create a `.env` file with the following settings:

```env
# Target website URL
TARGET_URL=https://example.com

# Queue threshold (position below which to open browser)
QUEUE_THRESHOLD=100

# Run in headless mode (true/false)
HEADLESS=true

# Email notification settings (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
NOTIFICATION_RECIPIENT=recipient@example.com
```

## Usage

1. Add your proxy IPs to `proxies.txt` (one per line, format: IP:PORT)
2. Configure your settings in `.env`
3. Run the bot:
   ```bash
   python queue_bot.py
   ```

## File Structure

- `queue_bot.py` - Main bot script
- `proxy_manager.py` - Manages proxy IPs
- `session_manager.py` - Handles queue sessions and monitoring
- `notifier.py` - Optional email notifications
- `proxies.txt` - List of proxy IPs
- `.env` - Configuration file

## Notes

- The bot uses Selenium with Chrome WebDriver
- Proxy IPs should be in the format IP:PORT
- Email notifications are optional
- The bot will automatically switch from headless to headed mode when queue position is below threshold

## Troubleshooting

1. If you get WebDriver errors, make sure Chrome is installed and up to date
2. For proxy issues, verify your proxy IPs are valid and in the correct format
3. For email notifications, ensure you're using an app-specific password if using Gmail 