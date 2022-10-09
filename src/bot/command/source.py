"""
Cog handling slash command configuring current channel for TTS.
All messages from configured channel will be read out.
"""

from disnake import CommandInteraction
from disnake.ext.commands import Cog, slash_command

from bot.channel.source_data import SourceChannelData

HELP_MESSAGE = "`/source` - toggle all messages from current channel for TTS"


class SourceCog(Cog):
    def __init__(self, source_channel_data: SourceChannelData) -> None:
        self._source_channel_data = source_channel_data

    @slash_command()
    async def source(self, interaction: CommandInteraction) -> None:
        """Toggle assignment of current channel for TTS"""
        channel_id = interaction.channel_id
        if channel_id in self._source_channel_data.get_channel_ids():
            self._source_channel_data.remove_channel_id(channel_id)
            await interaction.send("Channel removed")
        else:
            self._source_channel_data.add_channel_id(channel_id)
            await interaction.send("Channel added")
