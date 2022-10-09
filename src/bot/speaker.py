"""
Class handling reading out given texts to configured voice channel.
"""

from disnake import FFmpegPCMAudio, PCMVolumeTransformer
from disnake.utils import remove_markdown
from loguru import logger

from bot.channel.target import TargetChannel
from tts import convert_text_to_speech_file


class Speaker:
    def __init__(self, target_channel: TargetChannel) -> None:
        self._target_channel = target_channel

    async def speak(self, message: str) -> None:
        """Read given message to configured voice channel"""
        if not self._target_channel.is_connected():
            logger.info("Voice client not connected, skipping")
            return
        cleaned_message = self._clean_message(message)
        audio_file = convert_text_to_speech_file(cleaned_message)
        audio_source = PCMVolumeTransformer(FFmpegPCMAudio(audio_file))
        await self._target_channel.play(audio_source)

    def _clean_message(self, message: str) -> str:
        return remove_markdown(message)
