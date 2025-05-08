import logging
from datetime import datetime, timedelta
from pathlib import Path
from asyncio import run

from database.init import init
from telegrambot import AiogramBot
from settings.settings import BOT_TOKEN

LOG_DIR = Path(__file__).resolve().parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)


def cleanup_old_logs() -> None:
    """
    Deletes log files older than 183 days from the logs directory.

    Iterates through all .log files in the LOG_DIR directory, checks their
    modification time, and removes those older than the cutoff date.
    """
    cutoff_date = datetime.now() - timedelta(days=183)
    for log_file in LOG_DIR.glob('*.log'):
        try:
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < cutoff_date:
                log_file.unlink()
        except Exception as error:
            logging.warning(f'Ошибка при удалении {log_file}: {error}')


def setup_logging() -> None:
    """
    Configures logging for the application.

    Creates a log file named with the current date and time in the format
    'log_DD-MM-YYYY_HH-MM.log'. Logs are written both to this file and the console.
    """
    log_file = LOG_DIR / f"log_{datetime.now().strftime('%d-%m-%Y_%H-%M')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def main() -> None:
    """
    The main entry point of the bot application.

    - Sets up logging.
    - Cleans up old log files.
    - Initializes the database.
    - Starts the Telegram bot in polling mode.
    """
    setup_logging()
    cleanup_old_logs()

    logging.info('Запуск бота...')

    bot = AiogramBot(token=BOT_TOKEN)

    run(init())

    run(bot.run_polling())


if __name__ == '__main__':
    main()
