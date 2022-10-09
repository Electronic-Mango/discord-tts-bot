"""
Event Cog handling all incoming messages.
Messages can be send for TTS scheduling, based on configured TTS channels.
"""

from disnake import Client, Message
from disnake.ext.commands import Cog
from loguru import logger

from bot.channel.source_channel import SourceChannel
from bot.tts_scheduler import TtsScheduler


class OnMessageCog(Cog):
    def __init__(
        self,
        bot: Client,
        tts_scheduler: TtsScheduler,
        source_channel: SourceChannel,
    ) -> None:
        self._bot = bot
        self._tts_scheduler = tts_scheduler
        self._source_channel = source_channel

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Schedule messages from stored channels for TTS"""
        if not self._can_read_message(message):
            return
        logger.info(f"[{message.channel}] handling message [{message.id}]")
        self._tts_scheduler.add_message(message.content)

    def _can_read_message(self, message: Message) -> bool:
        return (
            message.channel.id in self._source_channel.get_channel_ids()
            and message.content
            and not message.interaction
        )
