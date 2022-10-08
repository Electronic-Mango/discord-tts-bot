"""
Event Cog handling all incoming messages.
"""

from disnake import Client, Message
from disnake.ext.commands import Cog
from loguru import logger

from bot.tts_scheduler import TtsScheduler


class OnMessage(Cog):
    def __init__(self, bot: Client, tts_scheduler: TtsScheduler) -> None:
        self._bot = bot
        self._tts_scheduler = tts_scheduler
        self._source_channel_ids = set()

    def add_source_channel_id(self, channel_id: int) -> None:
        self._source_channel_ids.add(channel_id)

    def remove_source_channel_id(self, channel_id: int) -> None:
        self._source_channel_ids.remove(channel_id)

    def has_source_channel_id(self, channel_id: int) -> None:
        return channel_id in self._source_channel_ids

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not self._can_read_message(message):
            return
        logger.info(f"[{message.channel}] handling message [{message.id}]")
        self._tts_scheduler.add_message(message.content)

    async def _can_read_message(self, message: Message) -> bool:
        return (
            self._source_channel_ids
            and message.channel.id in self._source_channel_ids
            and message.content
        )
