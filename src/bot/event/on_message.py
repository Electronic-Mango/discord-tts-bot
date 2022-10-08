"""
Event Cog handling all incoming messages.
Messages can be send for TTS scheduling, based on configured TTS channels.
"""

from disnake import Client, Message
from disnake.ext.commands import Cog
from loguru import logger

from bot.persistency import load_source_channels, save_source_channels
from bot.tts_scheduler import TtsScheduler


class OnMessageCog(Cog):
    def __init__(self, bot: Client, tts_scheduler: TtsScheduler) -> None:
        self._bot = bot
        self._tts_scheduler = tts_scheduler
        self._source_channel_ids = load_source_channels()

    def add_source_channel_id(self, channel_id: int) -> None:
        """Add new source channel ID"""
        self._source_channel_ids.add(channel_id)
        save_source_channels(self._source_channel_ids)

    def remove_source_channel_id(self, channel_id: int) -> None:
        """Remove given source channel ID"""
        self._source_channel_ids.remove(channel_id)
        save_source_channels(self._source_channel_ids)

    def is_source_channel_id(self, channel_id: int) -> None:
        """Check if given channel ID is already stored"""
        return channel_id in self._source_channel_ids

    def get_source_channels(self) -> str:
        """Return used voice channels info string"""
        source_channels = [self._bot.get_channel(id) for id in self._source_channel_ids]
        info = [f" - **{channel}** - {channel.guild}" for channel in source_channels]
        return "\n".join(info)

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Schedule messages from stored channels for TTS"""
        if not self._can_read_message(message):
            return
        logger.info(f"[{message.channel}] handling message [{message.id}]")
        self._tts_scheduler.add_message(message.content)

    def _can_read_message(self, message: Message) -> bool:
        return (
            self._source_channel_ids
            and message.channel.id in self._source_channel_ids
            and message.content
            and not message.interaction
        )
