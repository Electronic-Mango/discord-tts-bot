from logging import INFO, basicConfig
from os import environ

from dotenv import load_dotenv

from bot.bot import prepare_bot
from log_intercept import InterceptHandler

load_dotenv()
DISCORD_BOT_TOKEN = environ["DISCORD_BOT_TOKEN"]


def main():
    _configure_logging()
    bot = prepare_bot()
    bot.run(token=DISCORD_BOT_TOKEN)


def _configure_logging() -> None:
    basicConfig(handlers=[InterceptHandler()], level=INFO, force=True)


if __name__ == "__main__":
    main()
