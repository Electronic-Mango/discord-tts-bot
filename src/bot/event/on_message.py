"""
Event Cog handling all incoming messages.
"""

from os import environ

from bot.tts_scheduler import TtsScheduler
from disnake import Client, Message
from disnake.ext.commands import Cog
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
SOURCE_CHANNEL_IDS = list(map(int, environ["SOURCE_CHANNEL_IDS"].split(",")))


class OnMessage(Cog):
    def __init__(self, bot: Client, tts_scheduler: TtsScheduler) -> None:
        super().__init__()
        self._bot = bot
        self._tts_scheduler = tts_scheduler

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.channel.id not in SOURCE_CHANNEL_IDS or not message.content:
            return
        logger.info(f"[{message.channel}] handling message [{message.id}]")
        self._tts_scheduler.add_message(message.content)
