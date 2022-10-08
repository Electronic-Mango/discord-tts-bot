from os import environ
from typing import Any, Callable, Optional

from disnake import Client, FFmpegPCMAudio, PCMVolumeTransformer, VoiceClient
from dotenv import load_dotenv
from gtts import gTTS
from loguru import logger

load_dotenv()
TARGET_CHANNEL_ID = int(environ["TARGET_CHANNEL_ID"])
TEXT_LANGUAGE = environ["TEXT_LANGUAGE"]
VOICE_FILE_PATH = environ.get("VOICE_FILE_PATH", "voice_file.mp3")


class Speaker:
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._voice_client = None

    async def connect(self) -> None:
        self._voice_client = await self._get_voice_client()
        logger.info(f"Opened voice connection to [{self._voice_client}]")

    async def _get_voice_client(self) -> VoiceClient:
        return await self._bot.get_channel(TARGET_CHANNEL_ID).connect()

    def speak(
        self, message: str, after_playback: Callable[[Optional[Exception]], Any]
    ) -> None:
        if not self._voice_client:
            return
        speech = gTTS(message, lang=TEXT_LANGUAGE)
        speech.save(VOICE_FILE_PATH)
        audio_source = PCMVolumeTransformer(FFmpegPCMAudio(VOICE_FILE_PATH))
        self._voice_client.play(audio_source, after=after_playback)
