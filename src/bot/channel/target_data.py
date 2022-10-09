from bot.channel.target_channel import TargetChannel
from bot.persistency import load_target_channel, save_target_channel


class TargetChannelData:
    def __init__(self, target_channel: TargetChannel) -> None:
        self._target_channel = target_channel

    async def load_persistence(self) -> None:
        """Load stored target channel ID and open connection"""
        if channel_id := load_target_channel():
            await self._target_channel.connect(channel_id)

    async def set_channel_id(self, channel_id: int) -> None:
        """Set given channel ID as target voice channel and open connection"""
        save_target_channel(channel_id)
        await self._target_channel.connect(channel_id)

    async def unset_channel_id(self) -> None:
        """Unset given channel ID as target voice channel and close connection"""
        save_target_channel(None)
        await self._target_channel.disconnect()

    def get_channel_id(self) -> int:
        """Check if given channel ID is currently used"""
        return self._target_channel.get_channel_id()
