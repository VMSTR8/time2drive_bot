from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from tortoise import Tortoise

from handlers.start_handler import router as start_router
from handlers.search_handler import router as search_router
from handlers.excel_handler import router as excel_router


class AiogramBot:
    """
    Wrapper class for managing the lifecycle and configuration of an Aiogram-based Telegram bot.

    Attributes:
        token (str): The Telegram bot token.
        bot (Bot): The Aiogram Bot instance.
        dispatcher (Dispatcher): The Aiogram Dispatcher instance.
    """
    def __init__(self, token: str):
        """
        Initializes the AiogramBot with the given token.

        Args:
            token (str): Telegram bot token.
        """
        self.token = token

        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        self.dispatcher = Dispatcher()

    async def on_shutdown(self) -> None:
        """
        Gracefully closes all database connections on bot shutdown.
        """
        await Tortoise.close_connections()

    def shutdown_register(self) -> None:
        """
        Registers the shutdown callback to be called when the bot stops.
        """
        self.dispatcher.shutdown.register(self.on_shutdown)

    def setup_routes(self) -> None:
        """
        Includes all defined routers into the dispatcher.
        """
        self.dispatcher.include_router(start_router)
        self.dispatcher.include_router(search_router)
        self.dispatcher.include_router(excel_router)

    async def run_polling(self) -> None:
        """
        Starts the bot in polling mode after setting up routes and shutdown callbacks.
        """
        self.setup_routes()
        self.shutdown_register()
        await self.dispatcher.start_polling(self.bot)
