"""
Class handling reading out given texts to configured voice channel.
"""

from typing import Any, Callable, Optional

from disnake import Client, FFmpegPCMAudio, PCMVolumeTransformer
from disnake.utils import remove_markdown
from loguru import logger

from bot.persistency import load_target_channel, save_target_channel
from tts import convert_text_to_speech_file


class Speaker:
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._voice_client = None

    async def load_target_channel(self) -> None:
        """Load stored target voice channel from memory and connect to it"""
        if channel_id := load_target_channel():
            await self._connect_voice_client(channel_id)

    async def set_target_channel(self, channel_id: int) -> None:
        """Set new target voice channel and connect to it"""
        await self._disconnect_voice_client()
        await self._connect_voice_client(channel_id)
        save_target_channel(channel_id)

    def get_target_channel(self) -> str:
        """Return used voice channel info string"""
        target_channel = self._voice_client.channel
        return f"**{target_channel}** - {target_channel.guild}"

    def is_target_channel(self, channel_id: int) -> None:
        """Check if given channel ID matches channel used as TTS target"""
        return self._voice_client and channel_id == self._voice_client.channel.id

    async def clear_target_channel(self) -> None:
        """Clear and disconnect stored target channel"""
        await self._disconnect_voice_client()
        self._voice_client = None
        save_target_channel(None)

    async def _disconnect_voice_client(self) -> None:
        if self._voice_client:
            await self._voice_client.disconnect()

    async def _connect_voice_client(self, channel_id: int) -> None:
        self._voice_client = await self._bot.get_channel(channel_id).connect()

    def speak(self, message: str, after: Callable[[Optional[Exception]], Any]) -> None:
        """Read given message to configured voice channel"""
        if not self._voice_client:
            logger.info("Voice client not set, skipping")
            return
        cleaned_message = self._clean_message(message)
        audio_file = convert_text_to_speech_file(cleaned_message)
        audio_source = PCMVolumeTransformer(FFmpegPCMAudio(audio_file))
        self._voice_client.play(audio_source, after=after)

    def _clean_message(self, message: str) -> str:
        return remove_markdown(message)
