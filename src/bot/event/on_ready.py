"""
Event Cog logging information that bot is ready to internal logger.
"""

from disnake import Client
from disnake.ext.commands import Cog
from loguru import logger

from bot.speaker import Speaker


class OnReady(Cog):
    def __init__(self, bot: Client, speaker: Speaker) -> None:
        super().__init__()
        self._bot = bot
        self._speaker = speaker

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"[{self._bot.user}] ready, initializing speaker")
        await self._speaker.connect()
