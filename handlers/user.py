import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from utils.db.database import Database
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import LangChainException

class TelegramBot:
    def __init__(self, token: str, db_url: str):
        self.logger = logging.getLogger(__name__)
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.router = Router()
        self.db = Database(db_url)
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self._register_routes()
        self.dp.include_router(self.router)
        self.logger.info("TelegramBot initialized")

    def _register_routes(self):
        @self.router.message(Command(commands=['start']))
        async def start_handler(message: Message):
            user_id = message.from_user.id
            username = message.from_user.username or "Unknown"
            self.logger.info(f"Received /start from user_id={user_id}, username={username}")
            await message.answer("Привет! Я бот с ИИ. Напиши мне что-нибудь.")

        @self.router.message()
        async def ai_handler(message: Message):
            user_id = message.from_user.id
            self.logger.info(f"Received message from user_id={user_id}, content='{message.text}'")
            try:
                # Fetch projects from DB
                projects = self.db.get_info_from_db()
                if not projects:
                    self.logger.warning("No projects found in database")
                    await message.answer("No project data available to inform the response.")
                    return

                # Format projects into a context string
                context = "Наши проекты:\n"
                for project in projects:
                    context += (f"Название проекта: {project['name']}, ссылка {project['url']}.\n")

                # Create dynamic prompt with context
                #TODO дописать промпт на использование только существующих проектов и использование ссылок
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Ты полезный ассистент, знающий о следующих проектах:\n{context}\nОтвечай на русском языке."),
                    ("user", "{input}")
                ])
                chain = prompt | self.llm

                ai_response = await chain.ainvoke({"context": context, "input": message.text})
                await message.answer(ai_response.content)
            except LangChainException as e:
                self.logger.error(f"LangChain error in ai_handler: {e}")
                await message.answer("Ошибка при обращении к ИИ. Проверьте настройки API.")
            except Exception as e:
                self.logger.error(f"Error generating AI response: {e}")
                await message.answer("Ошибка генерации ответа. Попробуйте позже.")


    async def run(self):
        self.logger.info("Starting bot polling")
        await self.dp.start_polling(self.bot)
        self.logger.info("Bot polling stopped")