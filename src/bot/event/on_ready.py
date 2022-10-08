"""
Event Cog logging information that bot is ready to internal logger.
"""

from disnake import Client
from disnake.ext.commands import Cog
from loguru import logger

from bot.speaker import Speaker


class OnReadyCog(Cog):
    def __init__(self, bot: Client, speaker: Speaker) -> None:
        self._bot = bot
        self._speaker = speaker

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"[{self._bot.user}] initializing target TTS channel")
        await self._speaker.load_target_channel()
        logger.info(f"[{self._bot.user}] TTS initialization finished, ready")
