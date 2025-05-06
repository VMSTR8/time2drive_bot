from asyncio import run

from database.init import init
from telegrambot import AiogramBot
from settings.settings import BOT_TOKEN


def main() -> None:
    bot = AiogramBot(token=BOT_TOKEN)

    run(init())

    run(bot.run_polling())


if __name__ == '__main__':
    main()
