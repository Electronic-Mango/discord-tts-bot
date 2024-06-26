"""
Main module.
Configures logging and starts the bot.
"""

from logging import INFO, basicConfig

from bot.discord_bot import prepare_and_run_bot
from log_intercept import InterceptHandler


def main() -> None:
    _configure_logging()
    prepare_and_run_bot()


def _configure_logging() -> None:
    basicConfig(handlers=[InterceptHandler()], level=INFO, force=True)


if __name__ == "__main__":
    main()
