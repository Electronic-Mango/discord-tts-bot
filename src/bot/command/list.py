"""
Cog handling slash command listing all configured channels.
All source and target channels are listed.
"""

from disnake import Client, CommandInteraction, Thread
from disnake.abc import GuildChannel, PrivateChannel
from disnake.ext.commands import Cog, slash_command

from bot.channel.sources import SourceChannels
from bot.channel.target import TargetChannel

HELP_MESSAGE = "`/list` - list all configured channels"


class ListCog(Cog):
    def __init__(
        self,
        bot: Client,
        source_channels: SourceChannels,
        target_channel: TargetChannel,
    ) -> None:
        self._bot = bot
        self._source_channels = source_channels
        self._target_channel = target_channel

    @slash_command()
    async def list(self, interaction: CommandInteraction) -> None:
        """List all configured channels"""
        await interaction.response.defer()
        target_channel = self._get_target_channel_info()
        source_channels = self._get_source_channels_info()
        response = f"{target_channel}\n\n{source_channels}"
        await interaction.send(response)

    def _get_source_channels_info(self) -> str:
        channel_ids = self._source_channels.get_channel_ids()
        if not channel_ids:
            return "Sources: **not set**"
        channels = [self._bot.get_channel(channel_id) for channel_id in channel_ids]
        channel_infos = [f" - {self._format_channel(channel)}" for channel in channels]
        channel_info_str = "\n".join(channel_infos)
        return f"Sources:\n{channel_info_str}"

    def _get_target_channel_info(self) -> str:
        channel_id = self._target_channel.get_channel_id()
        if not channel_id:
            return "Target: **not set**"
        target_channel = self._bot.get_channel(channel_id)
        return f"Target: {self._format_channel(target_channel)}"

    def _format_channel(self, channel: GuildChannel | Thread | PrivateChannel) -> str:
        return f"**{channel}** - {channel.guild}"
