from asyncio import AbstractEventLoop, Event, Lock

from loguru import logger

from bot.speaker import Speaker


class TtsScheduler:
    def __init__(self, loop: AbstractEventLoop, speaker: Speaker) -> None:
        self._loop = loop
        self._speaker = speaker
        self._lock = Lock()

    def add_message(self, message: str) -> None:
        logger.info(f"Handling message [{message}]")
        self._loop.create_task(self._handle_message(message))

    async def _handle_message(self, message: str) -> None:
        async with self._lock:
            logger.info("Start handling message")
            event = Event()
            self._speaker.speak(message, lambda _: event.set())
            await event.wait()
            logger.info("Finish handling message")
