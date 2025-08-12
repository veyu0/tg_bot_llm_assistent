import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from utils.db.database import Database

class TelegramBot:
    def __init__(self, token: str, db_url: str):
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.router = Router()
        self.db = Database(db_url)
        self._register_routes()
        self.dp.include_router(self.router)
        self.logger.info("TelegramBot initialized")

    def _register_routes(self):
        @self.router.message(Command(commands=['start']))
        async def start_handler(message: Message):
            user_id = message.from_user.id
            username = message.from_user.username or "Unknown"
            self.logger.info(f"Received /start from user_id={user_id}, username={username}")
            await message.answer("Привет! Напиши мне что-нибудь.")

    async def run(self):
        self.logger.info("Starting bot polling")
        await self.dp.start_polling(self.bot)
        self.logger.info("Bot polling stopped")