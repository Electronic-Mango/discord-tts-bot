"""
Cog handling slash command listing all configured channels.
All source and target channels are listed.
"""

from disnake import Client, CommandInteraction, Thread
from disnake.abc import GuildChannel, PrivateChannel
from disnake.ext.commands import Cog, slash_command

from bot.channel.source_data import SourceChannelData
from bot.channel.target_data import TargetChannelData

HELP_MESSAGE = "`/list` - list all configured channels"


class ListCog(Cog):
    def __init__(
        self,
        bot: Client,
        source_channel_data: SourceChannelData,
        target_channel_data: TargetChannelData,
    ) -> None:
        self._bot = bot
        self._source_channel_data = source_channel_data
        self._target_channel_data = target_channel_data

    @slash_command()
    async def list(self, interaction: CommandInteraction) -> None:
        """List all configured channels"""
        await interaction.response.defer()
        target_channel = self._get_target_channel_info()
        source_channels = self._get_source_channel_info()
        response = f"Target: {target_channel}\n\nSources:\n{source_channels}"
        await interaction.send(response)

    def _get_source_channel_info(self) -> str:
        channel_ids = self._source_channel_data.get_channel_ids()
        channels = [self._bot.get_channel(channel_id) for channel_id in channel_ids]
        channel_infos = [f" - {self._format_channel(channel)}" for channel in channels]
        return "\n".join(channel_infos)

    def _get_target_channel_info(self) -> str:
        channel_id = self._target_channel_data.get_channel_id()
        target_channel = self._bot.get_channel(channel_id)
        return self._format_channel(target_channel)

    def _format_channel(self, channel: GuildChannel | Thread | PrivateChannel) -> str:
        return f"**{channel}** - {channel.guild}"
