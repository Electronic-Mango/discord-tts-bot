"""
Event Cog logging information that bot is ready to internal logger.
"""

from disnake import Client
from disnake.ext.commands import Cog
from loguru import logger


class OnReady(Cog):
    def __init__(self, bot: Client) -> None:
        super().__init__()
        self._bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"[{self._bot.user}] ready")
