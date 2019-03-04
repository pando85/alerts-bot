import os

ENVIRON_PREFIX = 'ALERTS_BOT_'

ALPHAVANTAGE_API_KEY: str = os.environ.get('ALPHAVANTAGE_API_KEY', 'SAWBBJUI4PULSS8R')
BOT_TOKEN: str = os.environ.get(f'{ENVIRON_PREFIX}TOKEN', '')
CHECK_PERIOD: int = int(os.environ.get(f'{ENVIRON_PREFIX}CHECK_PERIOD', 50))
LOG_LEVEL: str = os.environ.get(f'{ENVIRON_PREFIX}LOG_LEVEL', 'INFO')
STORAGE_FILE_PATH: str = os.environ.get(f'{ENVIRON_PREFIX}STORAGE_FILE_PATH', 'alerts_bot.json')
