from asyncio import Event

from disnake import AudioSource, Client

from bot.persistency import load_target_channel, save_target_channel


class TargetChannel:
    def __init__(self, bot: Client) -> None:
        self._bot = bot
        self._voice_client = None

    async def load_stored_channel(self) -> None:
        """Connect to channel based on stored channel ID"""
        if channel_id := load_target_channel():
            await self._open_voice_client(channel_id)

    async def connect(self, channel_id: int) -> None:
        """Open connection to voice channel with given channel ID"""
        await self._close_voice_client()
        await self._open_voice_client(channel_id)
        save_target_channel(channel_id)

    async def disconnect(self) -> None:
        """Disconnect from current voice channel"""
        await self._close_voice_client()
        self._voice_client = None
        save_target_channel(None)

    async def _close_voice_client(self) -> None:
        if self._voice_client:
            await self._voice_client.disconnect()

    async def _open_voice_client(self, channel_id: int) -> None:
        self._voice_client = await self._bot.get_channel(channel_id).connect()

    def is_connected(self) -> bool:
        """Is voice channel currently opened"""
        return self._voice_client and self._voice_client.is_connected()

    def get_channel_id(self) -> int | None:
        """Get channel ID of opened voice client, or None if voice client is closed"""
        return self._voice_client.channel.id if self.is_connected() else None

    async def play(self, audio_source: AudioSource) -> None:
        """Play given source and wait until playback is finished"""
        play_finished = Event()
        self._voice_client.play(audio_source, after=lambda _: play_finished.set())
        await play_finished.wait()
