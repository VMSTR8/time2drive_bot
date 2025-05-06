from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tortoise import Tortoise

from handlers.start_handler import router as start_router
from handlers.search_handler import router as search_router


class AiogramBot:

    def __init__(self, token: str):
        self.token = token

        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dispatcher = Dispatcher()

    async def on_shutdown(self) -> None:
        await Tortoise.close_connections()

    def shutdown_register(self) -> None:
        self.dispatcher.shutdown.register(self.on_shutdown)

    def setup_routes(self) -> None:
        self.dispatcher.include_router(start_router)
        self.dispatcher.include_router(search_router)

    async def run_polling(self) -> None:
        self.setup_routes()
        self.shutdown_register()
        await self.dispatcher.start_polling(self.bot)
