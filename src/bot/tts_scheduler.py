"""
Class scheduling TTS tasks.
Other modules can schedule strings to be read out simply by passing it to this class.
New asyncio task will be created for each string.
However, every task can access "speaker" class one at a time.
Otherwise, tasks would try to read out multiple strings at the same time.
"""

from asyncio import AbstractEventLoop, Lock

from loguru import logger

from bot.speaker import Speaker


class TtsScheduler:
    def __init__(self, loop: AbstractEventLoop, speaker: Speaker) -> None:
        self._loop = loop
        self._speaker = speaker
        self._lock = Lock()

    def add_message(self, message: str) -> None:
        """Create TTS task for given message"""
        logger.info(f"Schedule message [{message}]")
        self._loop.create_task(self._handle_message(message))

    async def _handle_message(self, message: str) -> None:
        async with self._lock:
            logger.info(f"Start handling message [{message}]")
            await self._speaker.speak(message)
            logger.info("Finished handling message")
