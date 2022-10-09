from bot.persistency import load_source_channels, save_source_channels


class SourceChannels:
    def __init__(self) -> None:
        self._source_channel_ids = load_source_channels()

    def add_channel_id(self, channel_id: int) -> None:
        """Store given channel ID as TTS source"""
        self._source_channel_ids.add(channel_id)
        save_source_channels(self._source_channel_ids)

    def remove_channel_id(self, channel_id: int) -> None:
        """Remove given channel ID from TTS sources"""
        self._source_channel_ids.remove(channel_id)
        save_source_channels(self._source_channel_ids)

    def get_channel_ids(self) -> set[int]:
        """Get a copy of stored source channel IDs"""
        return self._source_channel_ids.copy()
