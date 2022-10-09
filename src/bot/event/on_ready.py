"""
Event Cog initializing output TTS channel, once bot is connected.
If target channel is loaded up, then bot will automatically connect to this channel.
"""

from disnake.ext.commands import Cog
from loguru import logger

from bot.channel.target_channel import TargetChannel


class OnReadyCog(Cog):
    def __init__(self, target_channel: TargetChannel) -> None:
        self._target_channel = target_channel

    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Initializing target TTS channels")
        await self._target_channel.load_stored_channel()
        logger.info("TTS initialization finished, ready")
