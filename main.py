import asyncio
import os
import logging
from handlers.user import TelegramBot
from utils.parsing.parser import CaseParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("Starting application")
    TOKEN = os.getenv("TOKEN")
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    parser = CaseParser(db_url=DB_URL)
    parser.run()
    bot = TelegramBot(TOKEN, DB_URL)
    asyncio.run(bot.run())