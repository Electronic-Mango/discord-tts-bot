from os import environ
from typing import Any, Callable, Optional

from disnake import Client, FFmpegPCMAudio, PCMVolumeTransformer
from dotenv import load_dotenv
from gtts import gTTS
from loguru import logger

load_dotenv()
TEXT_LANGUAGE = environ["TEXT_LANGUAGE"]
VOICE_FILE_PATH = environ.get("VOICE_FILE_PATH", "voice_file.mp3")


class Speaker:
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._voice_client = None

    async def set_target_channel(self, channel_id: int) -> None:
        await self._disconnect_voice_client()
        await self._connect_voice_client(channel_id)

    def is_target_channel(self, channel_id: int) -> None:
        return channel_id == self._voice_client.channel.id

    async def clear_target_channel(self) -> None:
        await self._disconnect_voice_client()

    async def _disconnect_voice_client(self) -> None:
        if self._voice_client:
            await self._voice_client.disconnect()

    async def _connect_voice_client(self, channel_id: int) -> None:
        self._voice_client = await self._bot.get_channel(channel_id).connect()

    def speak(self, message: str, after: Callable[[Optional[Exception]], Any]) -> None:
        if not self._voice_client:
            logger.info("Voice client not set, skipping")
            return
        speech = gTTS(message, lang=TEXT_LANGUAGE)
        speech.save(VOICE_FILE_PATH)
        audio_source = PCMVolumeTransformer(FFmpegPCMAudio(VOICE_FILE_PATH))
        self._voice_client.play(audio_source, after=after)
