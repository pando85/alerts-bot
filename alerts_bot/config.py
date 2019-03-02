import os

ENVIRON_PREFIX = 'ALERTS_BOT_'

BOT_TOKEN: str = os.environ.get(f'{ENVIRON_PREFIX}BOT_TOKEN', '')
STORAGE_FILE_PATH: str = os.environ.get(f'{ENVIRON_PREFIX}STORAGE_FILE_PATH', 'alerts_bot.json')
